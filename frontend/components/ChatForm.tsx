"use client"
import { ChatContext } from "@/app/page";
import axios from "axios";
import { useContext, useRef } from "react";

const ChatForm = () => {
    const { onSubmit, conversationId, history } = useContext(ChatContext);
    const chatRef =  useRef<any>()

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        const input = chatRef.current.value;

        const resp = await axios.post(`/api/converse`, {
            input,
            conversationId,
        })

        if (input) {
            const { output, conversation_id: conversationId } = resp.data.data;
            const { question, response } = output

            onSubmit!([...history, { input: question, output: response }], conversationId);
            chatRef.current.value = "";
        }
    }

    return (
        <form action="#" onSubmit={handleSubmit}>
            <input
                ref={chatRef}
                name="chat"
                type="text"
                className="rounded rounded-full px-4 py-2 text-lg w-full border border-1 border-gray-600 bg-gray-800"
                placeholder="... Ask me anything"
                autoComplete="off"
            />
        </form>
    );
};

export default ChatForm
