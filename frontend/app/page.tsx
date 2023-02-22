"use client";
import ChatForm from "@/components/ChatForm";
import ChatHistory from "@/components/ChatHistory";
import { createContext, useEffect, useRef, useState } from "react";

interface Conversation {
    input: string;
    output: string;
}

interface ChatProviderProps {
    onSubmit: (response: Conversation[], conversationId: string) => void;
    history: Conversation[];
    conversationId: string | null;
}


export const ChatContext = createContext<ChatProviderProps>({
    history: [],
    onSubmit: () => {},
    conversationId: null,
});

export default function Home() {
    const [history, setHistory] = useState<Conversation[]>([]);
    const [conversationId, setConversationId] = useState<string | null>(null);
    const chatWindow = useRef<any>()

    useEffect(() => {
        chatWindow.current.scrollTop = chatWindow.current.scrollHeight;
    }, [history])

    const handleSubmit = (response: Conversation[], conversationId: string) => {
        setHistory(response); // add response to history
        setConversationId(conversationId); // update conversationId
    };

    return (
        <main className={`max-w-3xl flex h-screen gap-6 flex-col p-8 m-auto border-x border-slate-800`}>
            <ChatContext.Provider
                value={{ onSubmit: handleSubmit, history, conversationId }}
            >
                <section
                    ref={chatWindow}
                    id="responses"
                    className="w-full flex-1 overflow-y-auto"
                >
                    <ChatHistory />
                </section>
                <section id="chatbar" className="w-full">
                    <ChatForm />
                </section>
            </ChatContext.Provider>
        </main>
    );
}
