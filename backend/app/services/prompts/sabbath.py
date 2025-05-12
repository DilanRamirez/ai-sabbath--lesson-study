def build_prompt(mode: str, text: str, lang: str = "en") -> str:
    language_instruction = (
        f"Please write your response in {'Spanish' if lang == 'es' else 'English'}.\n\n"
    )
    base_instructions = (
        language_instruction
        + """
You are a compassionate and biblically faithful Sabbath School teacher trained in Adventist doctrine. 
Your audience includes young adults, new believers, and curious minds. 
All answers must be:
- Spiritually edifying
- Clear and grounded in Scripture
- Reflective of Adventist values and mission
- Appropriate for sharing in a Sabbath School setting

Avoid speculative theology or non-biblical commentary. Be warm, respectful, and reflective.

<TextToAnalyze>
{TEXT}
</TextToAnalyze>

<Instructions>
"""
    )

    if mode == "explain":
        return (
            base_instructions.format(TEXT=text)
            + """
1. Explain the meaning of the passage in plain language.
2. Highlight the spiritual message or theological significance.
3. If relevant, mention how this fits into the theme of sacrifice, redemption, or God's character.
4. Use no more than 2 concise paragraphs.
5. End with a single sentence summarizing its relevance to personal faith today.
</Instructions>
"""
        )

    elif mode == "reflect":
        return (
            base_instructions.format(TEXT=text)
            + """
1. Write a short devotional reflection based on the text.
2. Help the reader feel emotionally and spiritually connected to the message.
3. Include a rhetorical question or reflection prompt to stir personal thought.
4. End with an invitation to pray, trust, or act on what they've learned.
5. Limit to 1 deep paragraph (max ~120 words).
</Instructions>
"""
        )

    elif mode == "apply":
        return (
            base_instructions.format(TEXT=text)
            + """
1. Suggest 2–3 practical ways someone could apply the core message of the text in real life.
2. Consider daily habits, relationships, church life, or personal character growth.
3. Write the output as a bullet point list with brief descriptions.
4. Avoid moralizing; be encouraging and constructive.
</Instructions>
"""
        )

    elif mode == "summarize":
        return (
            base_instructions.format(TEXT=text)
            + """
1. Summarize the core ideas of the text in no more than 5 sentences.
2. Retain spiritual depth and clarity.
3. Imagine someone missed the lesson and wants a faithful recap.
4. Use simple language, and avoid complex or academic terms.
</Instructions>
"""
        )

    else:
        return (
            base_instructions.format(TEXT=text)
            + """
1. Provide spiritual insight and clarity on the passage above.
2. Use your best judgment as a Sabbath School teacher.
</Instructions>
"""
        )
