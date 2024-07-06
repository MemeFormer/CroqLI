Document the current state:

UPDATE TO DO LIST:

What's currently working (the menu on start up) 🆗

recently fixed:

1. search✅
2. chat✅
3. settings✅
- model settings✅
- top P✅
- max token✅
- temperature✅
4. system prompts✅❌

What needs to be fixed: cheat_sheet❌, or its placeholder for now. There is not even an item showing up in the settings anywhere so far. (Note to myself: IDK if it comes up on first run like we planned it (haven't tried yet)

**Any known issues or quirks:** 

- in topP/temp/token I only see the possible range, but I do not see what the current setting value is, neither     is there a suggestion to what the deault setting is.

- We should clearly show the setting in place WHILE in the editing process. there is also no confirmation when a    setting is entered. If I would accidently make a typo I wouldn't even know that it happened.

**Suggestion: show below each entry in the sub-menu AND in the main menu a highlighted (colored) entry of the setting that is currently set.**

- system prompt menu need rework (bad logic), and is also buggy. Again the "multiple line" issue when typing the    new system prompt

- you cant even select a prompt from the list to be used as such. "klicking" it just opens the prompt itself        which means 1.the title (used) which you can leave at it is or with enter get to 2 edit the system prompt.

- Don't like that you cannot choose to "mark" any of the prompts from the list and then get to choose what you      wanna do wit it. Like I want to use it/edit it(title and/or prompt/delete it/move up/move down/. But currently    there is no destiction really, and move up/down is missing at all
- Then outside of that should be (none of the above) and "add a new prompt to the list"
- at least the "add prompt" right now seems to basically work, I can give it a title, then write its content in     the next step (besides the multi line thing) and I see it then added to my list, so partially a success.

**RE chat mode:**

- the "safe" feature no longer working ->investigate
- exit let me change to the menu. Consider using a more consistent usage through all the modes and do it with       /menu and or /back (where "back" could switch to the model settings directly) whereas "menu" goes to menu. ---
- Also, make /m and /M working as well as /b and /B , same for "safe to markdown file" /s and /S instead or in      addition to just 'safe'

- haven't checked settings->API keys yet
   
