import { ReactNode } from "react";

export default function Tag({ type, children }: { type: string, children: ReactNode }) {
    return (
        <h2 className={'h-[22px] text-[14px] px-[6px] rounded-lg font-extrabold text-white dark:text-black flex items-center justify-center ' + (type === 'discount' ? 'bg-discount' : 'bg-cashback')}>{children}</h2>
    )
}
