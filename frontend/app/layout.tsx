import Flyout from "@/components/layout/Flyout";
import Navbar from "@/components/layout/navbar";
import "./globals.css";

interface Props {
    children: React.ReactNode;
}

const TopBar = () => {
    return (
        <div className="flex flex-col w-16 w-full">
            <span className="font-bold text-3xl font-serif">
                March 16th, 2023
            </span>
        </div>
    );
};

export default function RootLayout({ children }: Props): React.ReactElement {
    return (
        <html lang="en" data-theme="dark">
            {/*
            <head /> will contain the components returned by the nearest parent
            head.tsx. Find out more at https://beta.nextjs.org/docs/api-reference/file-conventions/head
        */}
            <head />
            <body>
                <Flyout>
                    <div className="h-screen flex overflow-hidden">
                        <Navbar />
                        <div className="w-full p-4 overflow-hidden flex flex-col gap-4">
                            <TopBar />
                            <div className="flex flex-1 gap-4 h-0">
                                <main className="flex flex-1">{children}</main>
                            </div>
                        </div>
                    </div>
                </Flyout>
            </body>
        </html>
    );
}
