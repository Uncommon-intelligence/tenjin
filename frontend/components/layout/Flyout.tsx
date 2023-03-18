import { VscAdd } from "react-icons/vsc";

type FlyoutProps = {
    children: React.ReactNode;
}

const Flyout: React.FC<FlyoutProps> = ({ children }) => {
    return (
        <div className="drawer drawer-end">
            <input id="flyout" type="checkbox" className="drawer-toggle" />
            <div className="drawer-content">
                {children}
            </div>
            <div className="drawer-side">
                <label htmlFor="flyout" className="drawer-overlay"></label>
                <div className="menu p-4 pt-6 w-[60vw] bg-base-100 text-base-content flex gap-2">
                    <h2 className="text-3xl font-bold font-serif">Cases</h2>
                    <div className="w-full h-[400px] bg-base-200 flex-1">

                    </div>
                    <div className="flex justify-end">
                        <button className="btn btn-ghost btn-sm">
                            <VscAdd size={18}/>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Flyout
