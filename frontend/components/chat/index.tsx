import React, { FC } from "react";
import ChatHistory from "../ChatHistory";
import ChatForm from "../ChatForm";

interface ChatProps {
    chatWindow: any;
}

const Chat: FC<ChatProps> = (props) => {
    const { chatWindow } = props;

    return (
        <div className="flex-1 flex flex-col space-y-4 max-w-[850px]">
            <section
                ref={chatWindow}
                id="responses"
                className="bg-base-300 flex-1 overflow-y-scroll"
            >
                <div className="max-h-[200px] p-4">
                    <ChatHistory />
                </div>
            </section>
            <section id="chatbar" className="w-full">
                <ChatForm />
            </section>
        </div>
    );
};

export { Chat };
