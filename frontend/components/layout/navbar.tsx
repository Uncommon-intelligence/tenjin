import { VscLibrary, VscNotebook, VscPlay } from "react-icons/vsc"

const Navbar = () => {
    return (
        <div className="bg-neutral flex flex-col w-16 items-center text-neutral-content">
            <div id="brand" className="p-4 font-bold text-xl">UI</div>
            <nav id="main-name" className="block flex-1 p-4">
                <ul className="flex flex-col gap-1">
                    <li>
                        <label htmlFor="flyout" className="btn opacity-80 hover:opacity-100">
                            <VscLibrary size={24}/>
                        </label>
                    </li>
                    <li>
                        <label htmlFor="flyout" className="btn opacity-80 hover:opacity-100">
                            <VscNotebook size={24}/>
                        </label>
                    </li>
                    <li>
                        <label htmlFor="flyout" className="btn opacity-80 hover:opacity-100">
                            <VscPlay size={24}/>
                        </label>
                    </li>
                </ul>
            </nav>
            <div id="settings" className="p-4">⚙️</div>
        </div>
    )
}

export default Navbar
