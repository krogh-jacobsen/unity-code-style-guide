# Implementing a Unity C# Style Guide as GitHub Copilot Instructions

Earlier in 2025 I helped update the [Unity C# Code Style guide for Unity 6](https://unity.com/resources/c-sharp-style-guide-unity-6). While there’s no single “correct” way to format Unity C# code, agreeing on a consistent style makes it much easier to build a clean, readable, and scalable codebase. That said, a style guide is only valuable if it’s actually put into practice.

## Implementing the style guide into your workflows
Since then, I’ve been experimenting with adapting the original style guide into my own and how to apply it in my current preferred setup on Mac with VS Code combined with GitHub Copilot. Copilot is incredibly helpful, but if you don’t give it clear instructions about your preferences, it will often default to generic suggestions. Fortunately, there are several ways to provide custom instructions so Copilot follows your style. One of the most effective is creating a .md instructions file.

## Why this version is different from the original guide
The original guide received positive feedback, but it also became clear that many users wanted more concrete examples and explanations for certain topics. Others, like myself, wanted to use AI tools like GitHub Copilot to help follow the guide but weren’t sure how to get the desired results most effectively without extensive prompting. Luckily, most modern IDEs offer ways to configure Copilot so it adheres to a specific style guide.


While this updated guide is still based on the original C# style guide and draws heavily from the
[Microsoft Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/), this version is intended to be more LLM‑friendly, pragmatic, and beginner‑friendly. It also includes some of my opinionated preferences which you can of course disregard or adapt to yours. 

While it’s aimed at Copilot, it also includes short explanations about why certain choices are made. It’s also intended to  serve as an educational resource that can inspire. Some points are repeated or phrased in different ways to give Copilot more examples and context. It might feel a bit verbose, but that helps reinforce the intent behind each rule so Copilot can make more informed decisions and you can follow along in the reasoning.

## How do I create my own instructions in Visual Code?
There are plenty of great articles on this and it has changed quite a few times, so I’ll just give you a quick summary. The short answer: create a copilot-instructions.md file in the root of your repository for GitHub Copilot to reference. Then simply add the instructions in .md (Markdown Documentation) formatting. Feel free to copy and paste whatever parts you find useful from my example. 

Previously, you had to go through a few extra configuration steps to get this working, but as of my latest version (November 2025), Copilot detects it automatically. The process is very similar for most LLMs and IDEs you might be using.

## A living document
Any code style guide should evolve over time and I’ll try not to make this one an exception :-)  I’m sure there are things I’ve missed, and I’m sure you’ll have suggestions that can make it even better. So let me know what works for you and what could be improved.

The goal here isn’t to claim there’s only one “correct” way to write code or to push too many personal preferences. I’m a fan of following industry standards, but I also work in education and ultimately, a good style guide is one that works for your needs. Those needs can vary a lot depending on whether you’re a solo developer or part of a larger team, whether you’re a beginner looking to learn, who values simplicity and readability, or senior engineer contributing to a large scale project codebase.

Use this guide as inspiration: adapt it, tweak it, or adopt it for your Unity projects however you like.

Happy coding!
