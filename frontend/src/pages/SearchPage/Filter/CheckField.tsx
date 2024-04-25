import React from "react";
import CheckBox from "../../../components/common/CheckBox";

type CheckFieldProps = {
    children: React.ReactNode;
    checked: boolean;
}

export default function CheckField({ children, checked }: CheckFieldProps) {

    return (
        <div className="h-[44px] custom-border flex px-3 items-center gap-3">
            <CheckBox checked={checked}>{children}</CheckBox>
        </div>
    )
}
