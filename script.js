"use strict";

// ========================================
// STUDY FROM HOME - LOGIN SYSTEM
// ========================================

const API_URL = "http://127.0.0.1:5000";

const loginForm = document.getElementById("loginForm");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");
const strengthBar = document.getElementById("strengthBar");
const message = document.getElementById("message");
const loginButton = document.querySelector(".login-btn");
const rememberCheckbox = document.getElementById("remember");
const forgotPassword = document.getElementById("forgotPassword");
const createAccount = document.getElementById("createAccount");
const googleLogin = document.getElementById("googleLogin");
const githubLogin = document.getElementById("githubLogin");

let isLoggingIn = false;
let isPasswordVisible = false;

// ========================================
// EMAIL VALIDATION
// ========================================

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ========================================
// PASSWORD VISIBILITY
// ========================================

if (togglePassword && passwordInput) {
    togglePassword.addEventListener("click", function () {
        isPasswordVisible = !isPasswordVisible;

        passwordInput.type = isPasswordVisible
            ? "text"
            : "password";

        togglePassword.textContent = isPasswordVisible
            ? "🙈"
            : "👁";
    });
}

// ========================================
// PASSWORD STRENGTH
// ========================================

if (passwordInput && strengthBar) {
    passwordInput.addEventListener("input", function () {
        const password = passwordInput.value;
        let strength = 0;

        if (password.length >= 6) {
            strength += 20;
        }

        if (password.length >= 10) {
            strength += 20;
        }

        if (/[A-Z]/.test(password)) {
            strength += 20;
        }

        if (/[a-z]/.test(password)) {
            strength += 15;
        }

        if (/[0-9]/.test(password)) {
            strength += 15;
        }

        if (/[^A-Za-z0-9]/.test(password)) {
            strength += 10;
        }

        strengthBar.style.width = strength + "%";

        if (strength < 40) {
            strengthBar.style.backgroundColor = "#ef4444";
        } else if (strength < 70) {
            strengthBar.style.backgroundColor = "#f59e0b";
        } else {
            strengthBar.style.backgroundColor = "#22c55e";
        }
    });
}

// ========================================
// EMAIL INPUT VALIDATION
// ========================================

if (emailInput) {
    emailInput.addEventListener("input", function () {
        const email = emailInput.value.trim();

        if (email === "") {
            emailInput.style.borderColor = "#e9d5ff";
        } else if (isValidEmail(email)) {
            emailInput.style.borderColor = "#22c55e";
        } else {
            emailInput.style.borderColor = "#ef4444";
        }
    });
}

// ========================================
// PASSWORD INPUT VALIDATION
// ========================================

if (passwordInput) {
    passwordInput.addEventListener("input", function () {
        const password = passwordInput.value;

        if (password === "") {
            passwordInput.style.borderColor = "#e9d5ff";
        } else if (password.length >= 6) {
            passwordInput.style.borderColor = "#22c55e";
        } else {
            passwordInput.style.borderColor = "#ef4444";
        }
    });
}

// ========================================
// LOGIN FORM
// ========================================

if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Prevent duplicate login requests
        if (isLoggingIn) {
            return;
        }

        const email = emailInput
            ? emailInput.value.trim()
            : "";

        const password = passwordInput
            ? passwordInput.value
            : "";

        // Validate empty fields
        if (!email || !password) {
            showMessage("Please fill in all fields.", "error");
            return;
        }

        // Validate email
        if (!isValidEmail(email)) {
            showMessage(
                "Please enter a valid email address.",
                "error"
            );

            if (emailInput) {
                emailInput.focus();
            }

            return;
        }

        // Validate password
        if (password.length < 6) {
            showMessage(
                "Password must contain at least 6 characters.",
                "error"
            );

            if (passwordInput) {
                passwordInput.focus();
            }

            return;
        }

        isLoggingIn = true;
        setLoading(true);

        try {
            const response = await fetch(
                API_URL + "/api/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );

            const result = await response.json();

            if (!response.ok || !result.success) {
                showMessage(
                    result.message || "Invalid email or password.",
                    "error"
                );

                isLoggingIn = false;
                setLoading(false);
                return;
            }

            // Check that user data exists
            if (!result.user) {
                showMessage(
                    "Login successful, but user data is missing.",
                    "error"
                );

                isLoggingIn = false;
                setLoading(false);
                return;
            }

            // Save logged-in user
            const userData = JSON.stringify(result.user);

            if (
                rememberCheckbox &&
                rememberCheckbox.checked
            ) {
                localStorage.setItem(
                    "studyFromHomeUser",
                    userData
                );

                localStorage.setItem(
                    "rememberLogin",
                    "true"
                );

                sessionStorage.removeItem(
                    "studyFromHomeUser"
                );
            } else {
                sessionStorage.setItem(
                    "studyFromHomeUser",
                    userData
                );

                localStorage.removeItem(
                    "studyFromHomeUser"
                );

                localStorage.removeItem(
                    "rememberLogin"
                );
            }

            showMessage(
                "Login successful. Opening dashboard...",
                "success"
            );

            isLoggingIn = false;
            setLoading(false);

            // Redirect only once
            setTimeout(function () {
                window.location.replace("dashboard.html");
            }, 500);

        } catch (error) {
            console.error("Login error:", error);

            isLoggingIn = false;
            setLoading(false);

            showMessage(
                "Backend is not running. Start app.py first.",
                "error"
            );
        }
    });
}

// ========================================
// LOADING BUTTON
// ========================================

function setLoading(isLoading) {
    if (!loginButton) {
        return;
    }

    loginButton.disabled = isLoading;

    if (isLoading) {
        loginButton.textContent = "Checking account...";
        loginButton.style.opacity = "0.75";
        loginButton.style.cursor = "wait";
    } else {
        loginButton.textContent = "Login to Account →";
        loginButton.style.opacity = "1";
        loginButton.style.cursor = "pointer";
    }
}

// ========================================
// MESSAGE
// ========================================

function showMessage(text, type) {
    if (!message) {
        alert(text);
        return;
    }

    message.style.display = "block";
    message.textContent = text;

    if (type === "error") {
        message.style.color = "#991b1b";
        message.style.backgroundColor = "#fee2e2";
        message.style.borderColor = "#fecaca";
    } else {
        message.style.color = "#166534";
        message.style.backgroundColor = "#dcfce7";
        message.style.borderColor = "#bbf7d0";
    }
}

// ========================================
// FORGOT PASSWORD
// ========================================

if (forgotPassword) {
    forgotPassword.addEventListener("click", function (event) {
        event.preventDefault();

        let email = emailInput
            ? emailInput.value.trim()
            : "";

        if (!email) {
            email = prompt(
                "Enter your registered email address:"
            );
        }

        if (!email) {
            return;
        }

        if (!isValidEmail(email)) {
            showMessage(
                "Enter a valid email address.",
                "error"
            );

            return;
        }

        showMessage(
            "Password reset is not configured yet.",
            "info"
        );
    });
}

// ========================================
// CREATE ACCOUNT
// ========================================

if (createAccount) {
    createAccount.addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = "register.html";
    });
}

// ========================================
// SOCIAL LOGIN
// ========================================

if (googleLogin) {
    googleLogin.addEventListener("click", function (event) {
        event.preventDefault();
        window.open(
            "https://www.google.com",
            "_blank",
            "noopener,noreferrer"
        );
    });
}

if (githubLogin) {
    githubLogin.addEventListener("click", function (event) {
        event.preventDefault();
        window.open(
            "https://github.com",
            "_blank",
            "noopener,noreferrer"
        );
    });
}