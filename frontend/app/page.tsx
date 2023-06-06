"use client";
import PDFViewer from "@/components/PDFViewer";
import { Chat } from "@/components/chat";
import { createContext, useEffect, useRef, useState } from "react";

export interface Source {
    page_content: string;
    lookup_str: string;
    lookup_index: number;
    metadata: {
        type: string;
        term: string;
        source: string;
        title: string;
        content: string;
    };
}

export type Conversation = {
    user?: string;
    assistant?: string;
    system?: string;
    sources: Source[];
};

interface ConversationResponse {
    data: Conversation[];
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

const STUB_MESSAGES: Conversation[] = [
    // TODO: Uncomment this for fast testing of styles. Should be deleted ASAP
    // {
    //     user: "Tim",
    //     assistant: "Frank",
    //     system: "wtf",
    //     sources: [
    //         {
    //             page_content: "aaaa",
    //             lookup_str: "aaaa",
    //             lookup_index: 2,
    //             metadata: {
    //                 type: "aaa",
    //                 term: "aaa",
    //                 source: "aaa",
    //                 title: "aaa",
    //                 content: "aaa",
    //             },
    //         },
    //     ],
    // },
    // {
    //     user: "AI",
    //     assistant:
    //         "Some content? I'm guessing this is the key for the content?",
    //     system: "wtf",
    //     sources: [
    //         {
    //             page_content: "aaaa",
    //             lookup_str: "aaaa",
    //             lookup_index: 2,
    //             metadata: {
    //                 type: "aaa",
    //                 term: "aaa",
    //                 source: "aaa",
    //                 title: "aaa",
    //                 content: "aaa",
    //             },
    //         },
    //     ],
    // },
];

export default function Home() {
    const [history, setHistory] = useState<Conversation[]>(STUB_MESSAGES);
    const [conversationId, setConversationId] = useState<string | null>(null);
    const chatWindow = useRef<any>();

    useEffect(() => {
        chatWindow.current.scrollTop = chatWindow.current.scrollHeight;
    }, [history]);

    useEffect(() => {
        console.log(conversationId);
    }, [conversationId]);

    const handleSubmit = (response: Conversation[], conversationId: string) => {
        setHistory(response);
        setConversationId(conversationId);
    };

    return (
        <ChatContext.Provider
            value={{ onSubmit: handleSubmit, history, conversationId }}
        >
            <Chat chatWindow={chatWindow} />

            <div className="flex-1 bg-base-300 p-4">
                <PDFViewer pdfURL="/example.pdf" />
            </div>
        </ChatContext.Provider>
    );
}
