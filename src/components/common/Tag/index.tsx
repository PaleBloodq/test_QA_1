import { ReactNode } from "react";

export default function Tag({ children }: { children: ReactNode }) {
    return (
        <h2 className='ml-4 h-[22px] text-[14px] px-[6px] bg-discount rounded-xl font-extrabold text-white dark:text-[#2C0C11] flex items-center justify-center'>{children}</h2>
    )
}
