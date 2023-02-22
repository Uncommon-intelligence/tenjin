import { ChatContext } from "@/app/page"
import { useContext } from "react"
import ReactMarkdown from "react-markdown"

const ChatHistory = () => {
    const { history } = useContext(ChatContext)

    return (
        <div className="flex flex-col gap-8">
            {history?.map(({input, output}) => (
                <div className="flex flex-col gap-2">
                    <strong className="text-xl text-gray-300">{input}</strong>
                    <ReactMarkdown children={output} />
                </div>
            ))}
        </div>
    )
}

export default ChatHistory
