import { ChatContext } from "@/app/page";
import { FC, useContext } from "react";
import MessageBubble from "./MessageBubble";

interface ChatMessagesProps {
    chatWindow: any;
}

const ChatMessages: FC<ChatMessagesProps> = (props) => {
    const { chatWindow } = props;
    const { history } = useContext(ChatContext);

    return (
        <section
            ref={chatWindow}
            id="responses"
            className="flex-1 overflow-y-scroll"
        >
            <div className="max-h-[200px] p-4">
                <div className="flex flex-col gap-[18px]">
                    {history?.map((message, index) => (
                        <MessageBubble key={index} {...message} />
                    ))}
                </div>
            </div>
        </section>
    );
};

export default ChatMessages;
