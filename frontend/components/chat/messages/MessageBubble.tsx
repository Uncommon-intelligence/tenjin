import React, { FC } from "react";
import { FaBookmark } from "react-icons/fa";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Source } from "@/app/page";
import Avatar from "./Avatar";
import SourceLink from "./SourceLink";

const POSITIONS = {
    LEFT: "LEFT",
    RIGHT: "RIGHT",
} as const;

type Position = (typeof POSITIONS)[keyof typeof POSITIONS];

interface MessageBubbleProps {
    user?: string;
    assistant?: string;
    sources: Source[];
}

interface BubbleThingyProps {
    position: Position;
}

const BubbleThingy: FC<BubbleThingyProps> = (props) => {
    const { position } = props;
    const sideBorderStyles =
        position === POSITIONS.LEFT
            ? "border-r-dark-400 border-t-dark-400 border-l-transparent"
            : "border-l-dark-300 border-t-dark-300 border-r-transparent";

    return (
        <div
            className={`w-0 h-0 border-[6px] ${sideBorderStyles} border-b-transparent`}
        />
    );
};

const MessageBubble: FC<MessageBubbleProps> = (props) => {
    const { user, assistant, sources } = props;

    // TODO: Replace this with better / clearer logic. This is for scaffolding purposes only.
    const isAiMessage = user === "AI";

    const wrapperStyle = isAiMessage ? "flex pl-[48px]" : "flex pr-[48px]";

    const backgroundStyle = isAiMessage
        ? "rounded-tr-none bg-dark-300"
        : "rounded-tl-none bg-dark-400";

    return (
        <div className={wrapperStyle}>
            {!isAiMessage && <BubbleThingy position={POSITIONS.LEFT} />}
            <div
                className={`flex flex-col grow gap-2 rounded-[6px] ${backgroundStyle} py-[18px] px-[18px]`}
            >
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
            {isAiMessage && <BubbleThingy position={POSITIONS.RIGHT} />}
        </div>
    );
};

export default MessageBubble;
