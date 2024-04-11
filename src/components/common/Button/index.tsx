
type ButtonProps = {
    children: string,
    onClick: () => void
}

export default function Button({ children, onClick }: ButtonProps) {
    return (
        <button className="w-full h-[50px] rounded-lg red-gradient text-white font-medium text-[15px] mt-5 active:scale-[0.99]" onClick={onClick}>
            {children}
        </button>
    )
}
