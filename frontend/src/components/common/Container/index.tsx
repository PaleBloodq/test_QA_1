export default function Container({ children }: { children: React.ReactNode }) {
    return (
        <div className='px-[15px] py-5 max-w-[560px] mx-auto'>
            {children && children}
        </div>
    )
}
