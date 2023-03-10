import { ChatContext } from "@/app/page";
import { useContext } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const SourceLink = ({ source }: any) => {
    if (!source) return null
    const { snippet, title, link } = source

    return (
        <a
            href={link}
            target="_blank"
            key={title}
            className="text-sm border border-gray-800 px-2 py-1 rounded-full hover:bg-gray-700 transition-all hover:border-gray-600 hover:text-white"
        >
            {title.slice(0, 20)}
        </a>
    )
}

const ChatHistory = () => {
    const { history } = useContext(ChatContext);

    return (
        <div className="flex flex-col gap-8">
            {history?.map(({ user, assistant, sources }) => (
                <div className="flex flex-col gap-2 border-b border-gray-800 pb-8">
                    <strong className="text-2xl text-gray-300 opacity-90">
                        {user}
                    </strong>
                    <strong className="mt-2 text-blue-500 font-semibold uppercase text-xs">Answer</strong>
                    <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        children={assistant!}
                        className="text-lg text-white"
                    />
                    <div className="flex gap-2 mt-4">
                        {sources?.map((source: any) => (<SourceLink source={source} />))}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ChatHistory;
