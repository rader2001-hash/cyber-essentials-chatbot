# Import Flask for the web interface
import re

from flask import Flask, render_template, request, jsonify, session

# Import the OpenAI library
from openai import OpenAI

# Import dotenv to load environment variables from the .env file
from dotenv import load_dotenv

# Import os to access environment variables
import os
# Import time for loading animation and delays
import time

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Connect to OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# System prompt - this tells OpenAI how to behave
SYSTEM_PROMPT = """
You are a Cyber Essentials readiness assessment assistant. 
Your job is to help organisations understand how ready they are for UK Cyber Essentials certification.

Follow these rules strictly:
- You lead the conversation at all times
- Ask one question at a time and wait for the answer
- Start by asking about the size of the organisation and what security measures they currently have in place
- Then assess each of the 5 Cyber Essentials control areas one by one:
  1. Firewalls
  2. Secure Configuration
  3. User Access Control
  4. Malware Protection
  5. Patch Management
- Ask clear simple questions a non technical person can understand
- Do not make compliance decisions yourself
- Do not go off topic
- Be friendly and professional
"""


# Initialise Flask app
app = Flask(__name__)
app.secret_key = "cyber_essentials_secret_key"
























# Cyber Essentials Rule Engine

def assess_firewall(answers):
    score = 0
    if answers.get("firewall_enabled") == "yes":
        score += 1
    if answers.get("firewall_configured") == "yes":
        score += 1
    if answers.get("firewall_default_deny") == "yes":
        score += 1
    return score, 3

def assess_secure_configuration(answers):
    score = 0
    if answers.get("default_passwords_changed") == "yes":
        score += 1
    if answers.get("unnecessary_software_removed") == "yes":
        score += 1
    if answers.get("auto_lock_enabled") == "yes":
        score += 1
    return score, 3

def assess_user_access_control(answers):
    score = 0
    if answers.get("admin_accounts_limited") == "yes":
        score += 1
    if answers.get("unique_accounts_per_user") == "yes":
        score += 1
    if answers.get("mfa_enabled") == "yes":
        score += 1
    return score, 3

def assess_malware_protection(answers):
    score = 0
    if answers.get("antivirus_installed") == "yes":
        score += 1
    if answers.get("antivirus_updated") == "yes":
        score += 1
    if answers.get("malware_scans_regular") == "yes":
        score += 1
    return score, 3

def assess_patch_management(answers):
    score = 0
    if answers.get("auto_updates_enabled") == "yes":
        score += 1
    if answers.get("software_up_to_date") == "yes":
        score += 1
    if answers.get("unsupported_software_removed") == "yes":
        score += 1
    return score, 3

def calculate_overall_score(answers):
    results = {}

    fw_score, fw_total = assess_firewall(answers)
    results["Firewalls"] = {
        "score": fw_score,
        "total": fw_total,
        "percentage": round((fw_score / fw_total) * 100),
        "passed": fw_score == fw_total
    }

    sc_score, sc_total = assess_secure_configuration(answers)
    results["Secure Configuration"] = {
        "score": sc_score,
        "total": sc_total,
        "percentage": round((sc_score / sc_total) * 100),
        "passed": sc_score == sc_total
    }

    uac_score, uac_total = assess_user_access_control(answers)
    results["User Access Control"] = {
        "score": uac_score,
        "total": uac_total,
        "percentage": round((uac_score / uac_total) * 100),
        "passed": uac_score == uac_total
    }

    mp_score, mp_total = assess_malware_protection(answers)
    results["Malware Protection"] = {
        "score": mp_score,
        "total": mp_total,
        "percentage": round((mp_score / mp_total) * 100),
        "passed": mp_score == mp_total
    }

    pm_score, pm_total = assess_patch_management(answers)
    results["Patch Management"] = {
        "score": pm_score,
        "total": pm_total,
        "percentage": round((pm_score / pm_total) * 100),
        "passed": pm_score == pm_total
    }

    total_score = sum(r["score"] for r in results.values())
    total_possible = sum(r["total"] for r in results.values())
    overall_percentage = round((total_score / total_possible) * 100)
    overall_passed = all(r["passed"] for r in results.values())

    return {
        "results": results,
        "overall_percentage": overall_percentage,
        "overall_passed": overall_passed
    }







    # Conversation flow
def run_assessment():
    while True:
        print("\n==========================================")
        print("   CYBER ESSENTIALS READINESS CHATBOT")
        print("==========================================\n")

        answers = {}
        unsure_flags = []
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Start the conversation
        messages.append({"role": "user", "content": "Please introduce yourself briefly and ask me about the size of my organisation and what kind of business I run."})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        print(f"Chatbot: {assistant_message}\n")

        # Get organisation context
        user_input = input("You: ").strip()
        messages.append({"role": "user", "content": user_input})

        # Acknowledge what the user said

       # Acknowledgement response
        acknowledgement = "Thank you for sharing that. The assessment is about to begin."
        messages.append({"role": "assistant", "content": acknowledgement})
        print(f"\nChatbot: {acknowledgement}")
        print("Please note this assessment may take 3 to 5 minutes to complete.\n")

        # Show tip once before questions begin
        print("*** Tip: For each question please answer yes, no, or unsure ***")
        print("*** Any other input will be asked to clarify ***\n")
        time.sleep(1)

        # Define sections
        sections = [
            {
                "title": "FIREWALL ASSESSMENT",
                "number": 1,
                "description": "Firewalls act as a barrier between your network and the internet, controlling what traffic is allowed in and out.",
                "questions": {
                    "firewall_enabled": "Do you have a firewall enabled on your network?",
                    "firewall_configured": "Is your firewall properly configured to filter traffic?",
                    "firewall_default_deny": "Is your firewall set to block all traffic by default unless explicitly allowed?"
                }
            },
            {
                "title": "SECURE CONFIGURATION ASSESSMENT",
                "number": 2,
                "description": "Secure configuration means making sure your devices and software are set up safely, with unnecessary features disabled and default settings changed.",
                "questions": {
                    "default_passwords_changed": "Have you changed all default passwords on your devices and software?",
                    "unnecessary_software_removed": "Have you removed any software or services that are not needed?",
                    "auto_lock_enabled": "Do your devices automatically lock after a period of inactivity?"
                }
            },
            {
                "title": "USER ACCESS CONTROL ASSESSMENT",
                "number": 3,
                "description": "User access control ensures that only the right people have access to the right systems, and that admin privileges are limited to those who need them.",
                "questions": {
                    "admin_accounts_limited": "Are admin accounts limited to only those who need them?",
                    "unique_accounts_per_user": "Does each user have their own unique account?",
                    "mfa_enabled": "Do you use multi-factor authentication on your accounts?"
                }
            },
            {
                "title": "MALWARE PROTECTION ASSESSMENT",
                "number": 4,
                "description": "Malware protection involves having tools in place to detect and block malicious software such as viruses, ransomware, and spyware.",
                "questions": {
                    "antivirus_installed": "Do you have antivirus or malware protection installed?",
                    "antivirus_updated": "Is your antivirus software kept up to date?",
                    "malware_scans_regular": "Do you run regular malware scans?"
                }
            },
            {
                "title": "PATCH MANAGEMENT ASSESSMENT",
                "number": 5,
                "description": "Patch management means keeping all your software and operating systems up to date so that known security vulnerabilities are fixed.",
                "questions": {
                    "auto_updates_enabled": "Are automatic updates enabled on your devices and software?",
                    "software_up_to_date": "Is all your software currently up to date?",
                    "unsupported_software_removed": "Have you removed any software that is no longer supported by the manufacturer?"
                }
            }
        ]

        # Go through each section
        for section in sections:
            print(f"\n==========================================")
            print(f"   [Section {section['number']} of 5] {section['title']}")
            print(f"==========================================")
            print(f"{section['description']}\n")
            time.sleep(0.5)

            for key, question in section["questions"].items():
                messages.append({"role": "user", "content": f"Ask the user this question in a friendly concise way: {question}"})
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                
                assistant_message = response.choices[0].message.content
                messages.append({"role": "assistant", "content": assistant_message})
                print(f"Chatbot: {assistant_message}\n")

                # Loop until valid input
                while True:
                    user_input = input("You: ").strip().lower()
                    
                    if user_input in ["yes", "no", "unsure"]:
                        break
                    else:
                        print("\nChatbot: Just to confirm, was that a yes, no, or unsure?\n")

                # Handle the answer
                if user_input == "yes":
                    answers[key] = "yes"
                    print("\nChatbot: Got it, noted!\n")
                elif user_input == "no":
                    answers[key] = "no"
                    print("\nChatbot: Understood, moving on.\n")
                elif user_input == "unsure":
                    answers[key] = "no"
                    unsure_flags.append((section["title"], question))
                    print("\nChatbot: No problem, we will flag that for your report.\n")

        # Loading animation
        print("\nChatbot: Thank you for completing the assessment!")
        time.sleep(1)
        print("\nAnalysing your responses", end="")
        for _ in range(3):
            time.sleep(0.7)
            print(".", end="", flush=True)
        print()
        print("Calculating your Cyber Essentials readiness score", end="")
        for _ in range(3):
            time.sleep(0.7)
            print(".", end="", flush=True)
        print()
        print("Generating your personalised report", end="")
        for _ in range(3):
            time.sleep(0.7)
            print(".", end="", flush=True)
        print("\n")

        # Run the rule engine
        output = calculate_overall_score(answers)

        # Raw results first
        print("\n==========================================")
        print("         RAW ASSESSMENT RESULTS")
        print("==========================================\n")
        for area, data in output["results"].items():
            status = "PASS" if data["passed"] else "FAIL"
            print(f"{area}: {data['percentage']}% [{status}]")
        print(f"\nOverall Score: {output['overall_percentage']}%")
        print(f"Cyber Essentials Ready: {'YES' if output['overall_passed'] else 'NO'}")

        # Breakdown and recommendations after raw results
        unsure_text = ""
        if unsure_flags:
            unsure_text = f"The user was unsure about the following: {unsure_flags}. For these suggest they investigate further with their IT support."

        messages.append({"role": "user", "content": f"Based on these Cyber Essentials assessment results, provide a breakdown for each control area. For each area that failed, write two to three plain English sentences explaining what the issue means and one clear recommendation on what to do. Keep it friendly and easy to understand for a non-technical person. Do not use bullet points or headers, just the area name, the explanation, and the recommendation. {unsure_text} Results: {output}"})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        breakdown = response.choices[0].message.content
        print(f"\n==========================================")
        print(f"      BREAKDOWN AND RECOMMENDATIONS")
        print(f"==========================================\n")
        print(f"{breakdown}\n")

        # Unsure summary grouped by category
        if unsure_flags:
            print("\n==========================================")
            print("         AREAS TO INVESTIGATE")
            print("==========================================")
            print("These are the questions you were unsure about.")
            print("We recommend looking into these with your IT")
            print("support or checking your settings directly.\n")
            current_section = None
            for section_title, question in unsure_flags:
                if section_title != current_section:
                    print(f"{section_title}:")
                    current_section = section_title
                print(f"  * {question}")
            print()

        # Restart option
        print("\n")
        restart = input("Chatbot: Would you like to run the assessment again? (yes/no): ").strip().lower()
        if restart != "yes":
            print("\nChatbot: Thank you for using the Cyber Essentials Readiness Chatbot. Good luck with your certification!\n")
            break

















# Route to serve the main chat page
@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if "messages" not in session:
        session["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]
    if "answers" not in session:
        session["answers"] = {}
    if "unsure_flags" not in session:
        session["unsure_flags"] = []
    if "stage" not in session:
        session["stage"] = "intro"
    if "question_index" not in session:
        session["question_index"] = 0
    if "current_section" not in session:
        session["current_section"] = ""

    messages = session["messages"]
    answers = session["answers"]
    unsure_flags = session["unsure_flags"]
    stage = session["stage"]
    question_index = session["question_index"]
    current_section = session["current_section"]

    all_questions = [
        ("firewall_enabled", "FIREWALL ASSESSMENT", "Firewalls act as a barrier between your network and the internet, controlling what traffic is allowed in and out.", "Do you have a firewall enabled on your network?"),
        ("firewall_configured", "FIREWALL ASSESSMENT", "Firewalls act as a barrier between your network and the internet, controlling what traffic is allowed in and out.", "Is your firewall properly configured to filter traffic?"),
        ("firewall_default_deny", "FIREWALL ASSESSMENT", "Firewalls act as a barrier between your network and the internet, controlling what traffic is allowed in and out.", "Is your firewall set to block all traffic by default unless explicitly allowed?"),
        ("default_passwords_changed", "SECURE CONFIGURATION ASSESSMENT", "Secure configuration means making sure your devices and software are set up safely, with unnecessary features disabled and default settings changed.", "Have you changed all default passwords on your devices and software?"),
        ("unnecessary_software_removed", "SECURE CONFIGURATION ASSESSMENT", "Secure configuration means making sure your devices and software are set up safely, with unnecessary features disabled and default settings changed.", "Have you removed any software or services that are not needed?"),
        ("auto_lock_enabled", "SECURE CONFIGURATION ASSESSMENT", "Secure configuration means making sure your devices and software are set up safely, with unnecessary features disabled and default settings changed.", "Do your devices automatically lock after a period of inactivity?"),
        ("admin_accounts_limited", "USER ACCESS CONTROL ASSESSMENT", "User access control ensures that only the right people have access to the right systems, and that admin privileges are limited to those who need them.", "Are admin accounts limited to only those who need them?"),
        ("unique_accounts_per_user", "USER ACCESS CONTROL ASSESSMENT", "User access control ensures that only the right people have access to the right systems, and that admin privileges are limited to those who need them.", "Does each user have their own unique account?"),
        ("mfa_enabled", "USER ACCESS CONTROL ASSESSMENT", "User access control ensures that only the right people have access to the right systems, and that admin privileges are limited to those who need them.", "Do you use multi-factor authentication on your accounts?"),
        ("antivirus_installed", "MALWARE PROTECTION ASSESSMENT", "Malware protection involves having tools in place to detect and block malicious software such as viruses, ransomware, and spyware.", "Do you have antivirus or malware protection installed?"),
        ("antivirus_updated", "MALWARE PROTECTION ASSESSMENT", "Malware protection involves having tools in place to detect and block malicious software such as viruses, ransomware, and spyware.", "Is your antivirus software kept up to date?"),
        ("malware_scans_regular", "MALWARE PROTECTION ASSESSMENT", "Malware protection involves having tools in place to detect and block malicious software such as viruses, ransomware, and spyware.", "Do you run regular malware scans?"),
        ("auto_updates_enabled", "PATCH MANAGEMENT ASSESSMENT", "Patch management means keeping all your software and operating systems up to date so that known security vulnerabilities are fixed.", "Are automatic updates enabled on your devices and software?"),
        ("software_up_to_date", "PATCH MANAGEMENT ASSESSMENT", "Patch management means keeping all your software and operating systems up to date so that known security vulnerabilities are fixed.", "Is all your software currently up to date?"),
        ("unsupported_software_removed", "PATCH MANAGEMENT ASSESSMENT", "Patch management means keeping all your software and operating systems up to date so that known security vulnerabilities are fixed.", "Have you removed any software that is no longer supported by the manufacturer?"),
    ]

    section_numbers = {
        "FIREWALL ASSESSMENT": 1,
        "SECURE CONFIGURATION ASSESSMENT": 2,
        "USER ACCESS CONTROL ASSESSMENT": 3,
        "MALWARE PROTECTION ASSESSMENT": 4,
        "PATCH MANAGEMENT ASSESSMENT": 5
    }

    ncsc_links = {
        "FIREWALL ASSESSMENT": "https://www.ncsc.gov.uk/collection/cyber-essentials/understanding-the-requirements/requirement-1-use-a-firewall-to-secure-your-internet-connection",
        "SECURE CONFIGURATION ASSESSMENT": "https://www.ncsc.gov.uk/collection/cyber-essentials/understanding-the-requirements/requirement-2-use-secure-settings-for-your-devices-and-software",
        "USER ACCESS CONTROL ASSESSMENT": "https://www.ncsc.gov.uk/collection/cyber-essentials/understanding-the-requirements/requirement-3-control-who-has-access-to-your-data-and-services",
        "MALWARE PROTECTION ASSESSMENT": "https://www.ncsc.gov.uk/collection/cyber-essentials/understanding-the-requirements/requirement-4-protect-your-devices-and-software-from-viruses-and-other-malware",
        "PATCH MANAGEMENT ASSESSMENT": "https://www.ncsc.gov.uk/collection/cyber-essentials/understanding-the-requirements/requirement-5-keep-your-devices-and-software-up-to-date"
    }

    response_messages = []
    is_complete = False
    results = None
    breakdown = None
    unsure_summary = None

    if stage == "intro":
        messages.append({"role": "user", "content": "Please introduce yourself briefly and ask me about the size of my organisation and what kind of business I run."})
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        intro_text = response.choices[0].message.content
        messages.append({"role": "assistant", "content": intro_text})
        response_messages.append({"type": "bot", "text": intro_text, "delay": 0})
        session["stage"] = "context"

    elif stage == "context":
        messages.append({"role": "user", "content": user_message})
        ack_text = "Thank you for sharing that. The assessment is about to begin. Please note this assessment may take 3 to 5 minutes to complete."
        tip_text = "For each question please answer yes, no, or unsure. Any other input will be asked to clarify."
        messages.append({"role": "assistant", "content": ack_text})

        response_messages.append({"type": "bot", "text": ack_text, "delay": 0})
        response_messages.append({"type": "tip", "text": tip_text, "delay": 800})
        response_messages.append({"type": "section", "title": all_questions[0][1], "number": 1, "description": all_questions[0][2], "delay": 1600})
        response_messages.append({"type": "bot", "text": all_questions[0][3], "delay": 2400})

        session["stage"] = "questions"
        session["current_section"] = all_questions[0][1]

    elif stage == "questions":
        user_input = user_message.strip().lower()

        if user_input in ["yes", "no", "unsure"]:
            key, section, description, question = all_questions[question_index]

            if user_input == "yes":
                answers[key] = "yes"
                ack = "Got it, noted!"
            elif user_input == "no":
                answers[key] = "no"
                ack = "Understood, moving on."
            elif user_input == "unsure":
                answers[key] = "no"
                unsure_flags.append((section, question))
                ack = "No problem, we will flag that for your report."

            response_messages.append({"type": "bot", "text": ack, "delay": 0})

            question_index += 1
            session["question_index"] = question_index
            session["answers"] = answers
            session["unsure_flags"] = unsure_flags

            if question_index >= len(all_questions):
                session["stage"] = "results"
                output = calculate_overall_score(answers)
                response_messages.append({"type": "bot", "text": "Thank you for completing the assessment. Compiling your results, please wait...", "delay": 0})
                
                # Build structured breakdown prompt
                breakdown_prompt = """Present the Cyber Essentials assessment results in the following exact format. Use plain text only. No markdown, no asterisks, no bold.
                Do not reproduce any raw data or Python dictionaries in your response under any circumstances.

Start with this line exactly:
The recommendations below are based on the official Cyber Essentials framework.

Then for each of the 5 control areas use this exact structure:

---

[AREA NAME]: [SCORE]% - [PASS or FAIL]

If PASS write exactly: Great work, this area meets Cyber Essentials requirements.

Do not include any raw data, dictionaries, or technical output in your response. Only write plain English text.

If FAIL write 2 to 3 plain English sentences explaining what the issue is and why it matters. Then write:

Recommendation: [one clear action the user should take]

Learn more: https://www.ncsc.gov.uk/cyberessentials/overview

"""
                unsure_text = ""
                if unsure_flags:
                    unsure_text = f"The user was unsure about: {unsure_flags}. Mention this where relevant."
               # Build a clean plain English summary to send to the AI
                area_summary = ""
                for area, data in output["results"].items():
                    status = "PASS" if data["passed"] else "FAIL"
                    area_summary += f"{area}: {data['percentage']}% - {status}\n"
               

                messages.append({"role": "user", "content": breakdown_prompt + unsure_text + f" Here are the results:\n{area_summary}"})


                response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
                
                breakdown_text = response.choices[0].message.content
                breakdown_text = re.sub(r'The user was unsure about[^.]*\.', '', breakdown_text).strip()

                if unsure_flags:
                    unsure_summary = {}
                    for sec_title, q in unsure_flags:
                        if sec_title not in unsure_summary:
                            unsure_summary[sec_title] = []
                        unsure_summary[sec_title].append(q)

                results = output
                breakdown = breakdown_text
                is_complete = True

            else:
                key, next_section, description, next_question = all_questions[question_index]
                delay = 400

                if next_section != current_section:
                    response_messages.append({"type": "transition", "text": "Moving to the next section...", "delay": delay})
                    delay += 2000
                    response_messages.append({"type": "section", "title": next_section, "number": section_numbers[next_section], "description": description, "delay": delay})
                    delay += 800
                    session["current_section"] = next_section
                else:
                    delay = 400

                response_messages.append({"type": "bot", "text": next_question, "delay": delay})

        else:
            response_messages.append({"type": "bot", "text": "Just to confirm, was that a yes, no, or unsure?", "delay": 0})

    session["messages"] = messages

    return jsonify({
        "messages": response_messages,
        "is_complete": is_complete,
        "results": results if is_complete else None,
        "breakdown": breakdown,
        "unsure_summary": unsure_summary if is_complete else None
    })


@app.route("/restart", methods=["POST"])
def restart():
    session.clear()
    session["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]
    session["answers"] = {}
    session["unsure_flags"] = []
    session["stage"] = "intro"
    session["question_index"] = 0
    session["current_section"] = ""
    return jsonify({"status": "ok"})



# Run Flask
if __name__ == "__main__":
    app.run(debug=True)



