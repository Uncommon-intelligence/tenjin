import Navbar from '@/components/layout/navbar'
import './globals.css'

interface Props {
    children: React.ReactNode
}

const TopBar = () => {
    return (
        <div className="flex flex-col w-16 w-full">
            <span className="font-bold text-3xl">March 16th, 2023</span>
        </div>
    )
}

const CaseList = () => {
    return (
        <div className="flex flex-col w-[200px] h-full w-32 space-y-4">
            <div className="flex-1 bg-base-200 p-4">
                cases
            </div>
            <button className='btn btn-primary'>Add Case</button>
        </div>
    )
}

export default function RootLayout({children}: Props): React.ReactElement {
  return (
    <html lang="en" data-theme="business">
        {/*
            <head /> will contain the components returned by the nearest parent
            head.tsx. Find out more at https://beta.nextjs.org/docs/api-reference/file-conventions/head
        */}
        <head />
        <body className='flex'>
            <Navbar />
            <div className='w-full h-screen p-4 overflow-hidden flex flex-col space-y-4'>
                <TopBar />
                <div className='flex flex-row h-full space-x-4'>
                    <CaseList />
                    <main className="flex-1">
                        {children}
                    </main>
                </div>
            </div>
        </body>
    </html>
  )
}
