import { FC } from "react";

interface SourceLinkProps {
    source: any;
}

const SourceLink: FC<SourceLinkProps> = (props) => {
    const { source } = props;

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

export default SourceLink;
