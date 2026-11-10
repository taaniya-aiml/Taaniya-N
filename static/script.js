
document.addEventListener("DOMContentLoaded", () => {
    const $ = (id) => document.getElementById(id);

    let currentProblem = null;
    let completed = new Set();

    function toast(message) {
        const element = $("toast");
        element.textContent = message;
        element.classList.add("show");
        setTimeout(() => element.classList.remove("show"), 3000);
    }

    function updateProgress() {
        const total = document.querySelectorAll(".problem-card").length;
        const count = completed.size;

        $("progressText").textContent =
            `${count} of ${total} practice problems completed`;

        $("progressBar").style.width =
            `${total ? (count / total) * 100 : 0}%`;

        $("summaryText").textContent = count
            ? `Great work! You completed ${count} problem(s) in this session.`
            : "Every expert starts somewhere. Try your first problem!";
    }

    $("menuToggle").addEventListener("click", () => {
        $("sidebar").classList.toggle("open");
    });

    document.querySelectorAll(".nav-link").forEach((link) => {
        link.addEventListener("click", () => {
            document.querySelectorAll(".nav-link").forEach((item) => {
                item.classList.remove("active");
            });
            link.classList.add("active");
            $("sidebar").classList.remove("open");
        });
    });

    const dialog = $("profileDialog");

    function openProfile() {
        if (!dialog.open) dialog.showModal();
    }

    $("profileButton").addEventListener("click", openProfile);
    $("editProfileButton").addEventListener("click", openProfile);
    $("closeProfile").addEventListener("click", () => dialog.close());

    function displayProfile(profile) {
        $("profileGreeting").textContent =
            profile.name ? `Welcome, ${profile.name}!` : "";

        $("domainLabel").textContent = `Domain: ${profile.domain}`;
        $("levelLabel").textContent = profile.level;
        $("companiesText").textContent = profile.companies;
        $("hoursText").textContent = `${profile.hours} hrs/week`;

        $("dailyPlan").textContent =
            profile.hours <= 2
                ? "Quick session: revise a concept and solve one problem."
                : profile.hours <= 7
                    ? "Focused practice: solve problems and review mistakes."
                    : "Plan regular sessions for revision, coding, and review.";
    }

    $("profileForm").addEventListener("submit", (event) => {
        event.preventDefault();

        const profile = {
            name: $("nameInput").value.trim(),
            domain: $("domainInput").value,
            level: $("levelInput").value,
            companies: $("companiesInput").value.trim(),
            hours: Number($("hoursInput").value)
        };

        if (!profile.companies) {
            toast("Enter target companies or type 'Not decided yet'.");
            return;
        }

        if (!Number.isInteger(profile.hours) ||
            profile.hours < 1 || profile.hours > 80) {
            toast("Weekly study hours must be between 1 and 80.");
            return;
        }

        displayProfile(profile);

        try {
            localStorage.setItem("cosmicCodeProfile", JSON.stringify(profile));
        } catch (error) {
            console.warn("Profile could not be saved in this browser.");
        }

        dialog.close();
        toast("Profile updated.");
    });

    try {
        const saved = JSON.parse(
            localStorage.getItem("cosmicCodeProfile") || "null"
        );

        if (saved) {
            $("nameInput").value = saved.name || "";
            $("domainInput").value = saved.domain || "C++";
            $("levelInput").value = saved.level || "Beginner";
            $("companiesInput").value = saved.companies || "";
            $("hoursInput").value = saved.hours || 5;
            displayProfile(saved);
        } else {
            openProfile();
        }
    } catch (error) {
        console.warn("Could not load the saved profile.");
    }

    function filterProblems() {
        const difficulty = $("difficultyFilter").value;
        const topic = $("topicFilter").value;

        document.querySelectorAll(".problem-card").forEach((card) => {
            const matchesDifficulty =
                difficulty === "All" ||
                card.dataset.difficulty === difficulty;

            const matchesTopic =
                topic === "All" || card.dataset.topic === topic;

            card.hidden = !(matchesDifficulty && matchesTopic);
        });
    }

    $("difficultyFilter").addEventListener("change", filterProblems);
    $("topicFilter").addEventListener("change", filterProblems);

    async function openProblem(problemId) {
        $("runStatus").textContent = "Loading problem...";
        $("runOutput").textContent = "";
        $("editorPanel").hidden = false;
        $("editorPanel").scrollIntoView({ behavior: "smooth" });

        try {
            const response = await fetch(`/api/problem/${encodeURIComponent(problemId)}`);
            const problem = await response.json();

            if (!response.ok) throw new Error(problem.error || "Problem not found.");

            currentProblem = problem;

            $("editorTitle").textContent = problem.title;
            $("problemDescription").textContent = problem.description;
            $("inputFormat").textContent = problem.input_format;
            $("outputFormat").textContent = problem.output_format;
            $("sampleInput").textContent = problem.examples[0]?.input || "";
            $("sampleOutput").textContent = problem.examples[0]?.output || "";
            $("codeEditor").value = problem.starter_code;
            $("customInput").value = "";
            $("runStatus").textContent = "Ready to run your code.";
        } catch (error) {
            $("runStatus").textContent = error.message;
        }
    }

    document.querySelectorAll(".solve-button").forEach((button) => {
        button.addEventListener("click", () => openProblem(button.dataset.id));
    });

    $("closeEditor").addEventListener("click", () => {
        $("editorPanel").hidden = true;
        currentProblem = null;
    });

    async function executeCode(action) {
        if (!currentProblem) {
            toast("Select a problem first.");
            return;
        }

        const button = action === "run"
            ? $("runCodeButton")
            : $("submitCodeButton");

        button.disabled = true;
        $("runStatus").textContent = "Compiling and running your C++ code...";
        $("runOutput").textContent = "";

        try {
            const response = await fetch("/api/run-code", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    problem_id: currentProblem.id,
                    source_code: $("codeEditor").value,
                    action: action
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Code execution failed.");
            }

            $("runStatus").textContent = data.message;

            $("runOutput").textContent = data.results.map((item, index) => {
                return [
                    `Test ${index + 1}: ${item.status}`,
                    `Input:\n${item.input}`,
                    `Expected:\n${item.expected}`,
                    `Your output:\n${item.output || "(no output)"}`,
                    item.error ? `Details:\n${item.error}` : ""
                ].filter(Boolean).join("\n");
            }).join("\n\n--------------------\n\n");

            if (action === "submit" && data.all_passed) {
                completed.add(currentProblem.id);
                updateProgress();
                toast("All tests passed! Problem completed.");
            } else if (data.all_passed) {
                toast("All tested cases passed!");
            }
        } catch (error) {
            $("runStatus").textContent = "Could not run code.";
            $("runOutput").textContent = error.message;
        } finally {
            button.disabled = false;
        }
    }

    $("runCodeButton").addEventListener("click", () => executeCode("run"));
    $("submitCodeButton").addEventListener("click", () => executeCode("submit"));

    $("sendQuestion").addEventListener("click", async () => {
        const question = $("mentorQuestion").value.trim();

        if (!question) {
            toast("Type a question first.");
            return;
        }

        $("mentorMessage").textContent =
            "The AI Mentor service is not connected yet. Please use the practice editor to test your code.";
    });

    const now = new Date();
    const dateElement = document.createElement("p");
    dateElement.textContent = now.toLocaleDateString(undefined, {
        weekday: "short",
        day: "numeric",
        month: "short",
        year: "numeric"
    });
    dateElement.className = "date-pill";
    $("profileGreeting").after(dateElement);

    updateProgress();
});
