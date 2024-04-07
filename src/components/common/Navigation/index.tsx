import { Link } from "react-router-dom";
import Search from "./Search";
import ToCartButton from "./ToCartButton";

export default function Navigation() {
    return (
        <div className="w-full h-[50px] flex gap-[14px] mb-6">
            <Search />
            <Link to="#">
                <button className="w-[50px] h-[50px] flex items-center justify-center custom-border">
                    <svg className="fill-secondary-light dark:fill-white" width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M14.9999 7.2857C14.9999 5.62801 13.6576 4.2857 11.9999 4.2857C10.3422 4.2857 8.99993 5.62801 8.99993 7.2857C8.99993 8.94338 10.3422 10.2857 11.9999 10.2857C13.6576 10.2857 14.9999 8.94338 14.9999 7.2857ZM16.7142 7.2857C16.7142 9.89016 14.6044 12 11.9999 12C9.39547 12 7.28564 9.89016 7.28564 7.2857C7.28564 4.68124 9.39547 2.57141 11.9999 2.57141C14.6044 2.57141 16.7142 4.68124 16.7142 7.2857ZM5.99993 17.6939C5.99993 18.5025 5.93125 18.4286 6.39069 18.4286H18.0377C18.4972 18.4286 18.4285 18.5025 18.4285 17.6939C18.4285 15.7326 15.5965 14.5714 12.2142 14.5714C8.83195 14.5714 5.99993 15.7326 5.99993 17.6939ZM4.28564 17.6939C4.28564 14.368 7.97043 12.8571 12.2142 12.8571C16.458 12.8571 20.1428 14.368 20.1428 17.6939C20.1428 19.4222 19.4733 20.1428 18.0377 20.1428H6.39069C4.95517 20.1428 4.28564 19.4222 4.28564 17.6939Z" />
                    </svg>
                </button>
            </Link>
            <ToCartButton />
        </div>
    )
}
