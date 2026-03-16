/**
 * LectureLLM — Lecture Mode for Live Lecture AI
 * 
 * Unlike interview mode (generating what YOU should say),
 * lecture mode LISTENS to the professor and helps you UNDERSTAND.
 * 
 * Features:
 * - Real-time concept explanations
 * - Question answering from lecture context
 * - Auto-generated study notes
 * - "Explain like I'm 5" simplifications
 */

import { LLMHelper } from '../LLMHelper';

// ==========================================
// LECTURE MODE PROMPTS
// ==========================================

export const LECTURE_SYSTEM_PROMPT = `You are a brilliant study companion sitting next to a student in a live lecture.

YOUR ROLE:
- You can hear everything the professor says (via the transcript)
- The student can quietly ask you questions about what's being taught
- You explain concepts clearly, concisely, and at the right level
- You connect new concepts to things already covered in this lecture

RULES:
1. Base ALL answers on what the professor has actually said in the transcript
2. If the professor hasn't covered something yet, say so: "The professor hasn't gotten to that yet, but generally..."
3. Be concise — the student is in class and needs quick answers
4. Use analogies and simple language to clarify complex ideas
5. Format with markdown: **bold** key terms, \`code\`, math as $LaTeX$
6. If a concept builds on something said earlier, reference it
7. Never make up things the professor said

ANSWER LENGTH:
- Quick clarification: 1-2 sentences
- Concept explanation: 3-5 sentences max
- Code/math walkthrough: as long as needed, but commented

WHAT YOU'RE GREAT AT:
- "What did they mean by X?"
- "Can you explain that last part simpler?"
- "How does X relate to Y they mentioned earlier?"
- "Give me the key formula/equation"
- "Summarize the last 5 minutes"
- "What's the main takeaway so far?"`;

export const LECTURE_WHAT_TO_ASK_PROMPT = `Based on the lecture transcript so far, generate 3 insightful questions the student could ask (either to themselves for deeper understanding, or to the professor).

RULES:
- Questions should probe deeper understanding, not surface-level recall
- Focus on connections between concepts, edge cases, or practical applications
- Each question: 1 sentence, clear and specific
- Format as numbered list (1. 2. 3.)`;

export const LECTURE_NOTES_PROMPT = `Generate structured study notes from this lecture transcript.

FORMAT:
## Key Concepts
- **Concept**: Brief explanation

## Important Formulas/Code
- Listed with context

## Connections
- How concepts relate to each other

## Questions to Review
- Things to study further

RULES:
- Only include what was actually discussed
- Be concise but complete
- Highlight what the professor emphasized
- Note any examples or analogies used`;

export const LECTURE_EXPLAIN_PROMPT = `The student wants a simpler explanation of a concept from the lecture.

RULES:
- Use an analogy if helpful
- Break it into small steps
- Use everyday language
- Keep it to 3-5 sentences max
- Reference what the professor said if relevant`;

/**
 * Process a lecture Q&A request
 */
export async function lectureModeAnswer(
    helper: LLMHelper,
    transcript: string,
    question: string,
    provider?: string
): Promise<string> {
    const systemPrompt = LECTURE_SYSTEM_PROMPT;
    const userMessage = `=== LECTURE TRANSCRIPT ===\n${transcript}\n=== END TRANSCRIPT ===\n\nStudent's question: ${question}`;
    
    return helper.chat(systemPrompt, userMessage, provider);
}

/**
 * Generate study notes from transcript
 */
export async function lectureNotes(
    helper: LLMHelper,
    transcript: string,
    provider?: string
): Promise<string> {
    const systemPrompt = LECTURE_NOTES_PROMPT;
    const userMessage = `Generate study notes from this lecture:\n\n${transcript}`;
    
    return helper.chat(systemPrompt, userMessage, provider);
}

/**
 * Generate thought-provoking questions
 */
export async function lectureQuestions(
    helper: LLMHelper,
    transcript: string,
    provider?: string
): Promise<string> {
    const systemPrompt = LECTURE_WHAT_TO_ASK_PROMPT;
    const userMessage = `Based on this lecture so far:\n\n${transcript}`;
    
    return helper.chat(systemPrompt, userMessage, provider);
}
