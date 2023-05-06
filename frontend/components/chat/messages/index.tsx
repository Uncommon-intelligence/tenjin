import { ChatContext } from "@/app/page";
import { FC, useContext } from "react";
import { FaBookmark } from "react-icons/fa";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatMessagesProps {
    chatWindow: any;
}

const SourceLink: FC = ({ source }: any) => {
    if (!source) return null;
    const { snippet, title, link } = source;

    return (
        <a
            href={link}
            target="_blank"
            rel="noreferrer"
            key={title}
            className="text-sm text-secondary border border-secondary px-2 py-1 rounded-full hover:bg-primary transition-all hover:text-primary-content whitespace-nowrap overflow-hidden overflow-ellipsis"
        >
            {title}
        </a>
    );
};

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
                    {history?.map(({ user, assistant, sources }, index) => (
                        <div
                            key={index}
                            className="flex flex-col gap-2 border-b border-[rgba(133,133,133,0.3)] pb-8"
                        >
                            <div className="flex gap-2">
                                <strong className="text-xl text-primary-content font-serif block flex-1">
                                    {user}
                                </strong>
                                <div
                                    className="tooltip tooltip-left"
                                    data-tip="Save response"
                                >
                                    <button className="p-0 m-0 opacity-20 hover:opacity-100 h-5">
                                        <FaBookmark />
                                    </button>
                                </div>
                            </div>
                            <strong className="mt-2 text-info font-semibold uppercase text-xs">
                                Answer
                            </strong>
                            <div className="prose max-w-full">
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    className=""
                                >
                                    {assistant!}
                                </ReactMarkdown>
                            </div>
                            {sources?.length > 0 && (
                                <div className="mt-4">
                                    <strong className="mt-2 text-info font-semibold uppercase text-xs">
                                        Sources
                                    </strong>
                                    <div className="flex gap-2 mt-4">
                                        {sources?.map((source: any, index) => (
                                            <SourceLink
                                                key={index}
                                                source={source}
                                            />
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default ChatMessages;
