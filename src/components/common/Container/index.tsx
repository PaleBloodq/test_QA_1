export default function Container({ children }: { children: React.ReactNode }) {
    return (
        <div className="w-full max-w-[640px] mx-auto px-[15px] py-7">
            {children}
        </div>
    )
}
