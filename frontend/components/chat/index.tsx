import React, { FC } from "react";
import ChatMessages from "./messages";
import ChatForm from "./ChatForm";

interface ChatProps {
    chatWindow: any;
}

const Chat: FC<ChatProps> = (props) => {
    const { chatWindow } = props;

    return (
        <div className="basis-[800px] shrink-0 flex flex-col">
            <ChatMessages chatWindow={chatWindow} />
            <section id="chatbar" className="w-full">
                <ChatForm />
            </section>
        </div>
    );
};

export { Chat };
