"use client"
import { ChatContext } from "@/app/page";
import axios from "axios";
import { useContext, useRef } from "react";
import { FaPaperPlane } from "react-icons/fa";

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
            const { data, conversation_id: conversationId } = resp.data

            onSubmit!(data, conversationId);
            chatRef.current.value = "";
        }
    }

    return (
        <form action="#" onSubmit={handleSubmit}>
            <div className="form-control">
                <div className="input-group">
                    <input
                        ref={chatRef}
                        name="chat"
                        type="text"
                        className="input input-bordered input-primary w-full outline-none"
                        placeholder="... Ask me anything"
                        autoComplete="off"
                    />
                    <button className="btn">
                        <FaPaperPlane />
                    </button>
                </div>
            </div>
        </form>
    );
};

export default ChatForm
