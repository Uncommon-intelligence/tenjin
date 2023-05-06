import { ChatContext } from "@/app/page";
import { FC, useContext } from "react";
import UserMessage from "./UserMessage";

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
                <div className="flex flex-col gap-8">
                    {history?.map((message, index) => (
                        <UserMessage key={index} {...message} />
                    ))}
                </div>
            </div>
        </section>
    );
};

export default ChatMessages;
