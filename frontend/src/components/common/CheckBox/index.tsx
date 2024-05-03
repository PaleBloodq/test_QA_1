type Props = {
    children: React.ReactNode,
    checked: boolean,
    onClick?: () => void
}

export default function CheckBox({ children, checked, onClick }: Props) {
    return (
        <div onClick={onClick ? onClick : () => { }} className="flex gap-3">
            {checked ? <svg width="21" height="21" viewBox="0 0 21 21" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="21" height="21" rx="6" fill="#B13430" />
                <path d="M8.91661 12.9203L6.12314 10.1268C5.91703 9.92068 5.58286 9.92068 5.37675 10.1268C5.17064 10.3329 5.17064 10.6671 5.37675 10.8732L8.54342 14.0398C8.74953 14.246 9.0837 14.246 9.28981 14.0398L15.6231 7.70651C15.8293 7.5004 15.8293 7.16623 15.6231 6.96012C15.417 6.75401 15.0829 6.75401 14.8767 6.96012L8.91661 12.9203Z" fill="white" />
            </svg>
                : <svg className="stroke-[#E7E7E8] dark:stroke-[#FFFFFF36]" width="21" height="21" viewBox="0 0 21 21" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0.5" y="0.5" width="20" height="20" rx="5.5" fill="none" />
                </svg>
            }
            <p className="text-subtitle-info cursor-pointer select-none">{children}</p>
        </div>
    )
}
