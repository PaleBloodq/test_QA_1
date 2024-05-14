export default function Container({ children }: { children: React.ReactNode }) {
    return (
        <div className='px-[15px] py-5 max-w-[560px] mx-auto min-h-[100vh]'>
            {children && children}
        </div>
    )
}
