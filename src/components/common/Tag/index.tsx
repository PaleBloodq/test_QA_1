import { ReactNode } from "react";

export default function Tag({ type, children }: { type: string, children: ReactNode }) {
    return (
        <h2 className={'ml-4 h-[22px] text-[14px] px-[6px] rounded-lg font-extrabold text-white flex items-center justify-center ' + (type === 'discount' ? 'bg-discount' : 'bg-cashback')}>{children}</h2>
    )
}
