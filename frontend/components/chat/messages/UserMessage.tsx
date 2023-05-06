import React, { FC } from "react";
import { FaBookmark } from "react-icons/fa";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Source } from "@/app/page";
import Avatar from "./Avatar";

interface UserMessageProps {
    user?: string;
    assistant?: string;
    sources: Source[];
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

const BubbleThingy: FC = () => (
    <div className="w-0 h-0 border-[6px] border-r-dark-400 border-l-transparent border-t-dark-400 border-b-transparent" />
);

const UserMessage: FC<UserMessageProps> = (props) => {
    const { user, assistant, sources } = props;

    return (
        <div className="flex pr-[48px]">
            <BubbleThingy />
            <div className="flex flex-col grow gap-2 rounded-[6px] rounded-tl-none bg-dark-400 py-[18px] px-[18px]">
                <div className="flex">
                    <Avatar user={user} />
                    <div className="px-[18px] grow">
                        <ReactMarkdown remarkPlugins={[remarkGfm]} className="">
                            {assistant!}
                        </ReactMarkdown>
                    </div>
                    <div
                        className="tooltip tooltip-left"
                        data-tip="Save response"
                    >
                        <button className="p-0 m-0 opacity-20 hover:opacity-100 h-5">
                            <FaBookmark />
                        </button>
                    </div>
                </div>
                {sources?.length > 0 && (
                    <div className="mt-4">
                        <strong className="mt-2 text-info font-semibold uppercase text-xs">
                            Sources
                        </strong>
                        <div className="flex gap-2 mt-4">
                            {sources?.map((source: any, index: number) => (
                                <SourceLink key={index} source={source} />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UserMessage;
