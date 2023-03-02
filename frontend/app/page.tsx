"use client";
import ChatForm from "@/components/ChatForm";
import ChatHistory from "@/components/ChatHistory";
import { createContext, useEffect, useRef, useState } from "react";

interface Source {
    page_content: string;
    lookup_str: string;
    lookup_index: number;
    metadata: {
        type: string;
        term: string;
        source: string;
        title: string;
        content: string;
    }
}

type Conversation = {
    user?: string;
    assistant?: string;
    system?: string;
    sources: Source[];
}

interface ConversationResponse {
    data: Conversation[]
    conversation_id: string;
}

interface ChatProviderProps {
    onSubmit: (response: ConversationResponse, conversationId: string) => void;
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

    useEffect(() => {
        console.log(conversationId)
    }, [conversationId])

    const handleSubmit = (response: Conversation[], conversationId: string) => {
        setHistory(response);
        setConversationId(conversationId);
    };

    return (
        <main className={`max-w-4xl flex h-screen gap-6 flex-col m-auto border-x border-slate-800`}>
            <ChatContext.Provider
                value={{ onSubmit: handleSubmit, history, conversationId }}
            >
                <section
                    ref={chatWindow}
                    id="responses"
                    className="w-full flex-1 overflow-y-auto p-8"
                >
                    <ChatHistory />
                </section>
                <section id="chatbar" className="w-full p-8">
                    <ChatForm />
                </section>
            </ChatContext.Provider>
        </main>
    );
}
