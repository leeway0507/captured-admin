import "./custom-input.css";
import React from "react";

interface customInputProps {
    label: string;
    type: string;
    value: string;
    setValue: (value: string) => void;
    id: string;
    placeholder?: string | undefined;
    info: string;
    checkPolicy: (value: string) => boolean | undefined;
    [rest: string]: any;
}

const CustomInput: React.FC<customInputProps> = (props: customInputProps) => {
    const { label, type, value, setValue, id, placeholder, info, checkPolicy, ...rest } = props;
    return (
        <div className="relative my-2">
            <input
                type={type}
                className={`peer custom-input-class ${!checkPolicy(value) && "border-orange-600"}`}
                onChange={(e) => {
                    setValue(e.target.value);
                }}
                value={value}
                id={id}
                placeholder={placeholder ?? "empty"}
                {...rest}
            />
            <label htmlFor={id} className="custom-label-class">
                {label}
            </label>
            <div className={`text-xs  ${checkPolicy(value) ? "text-white" : "text-orange-600"}`}>{info}</div>
        </div>
    );
};

export default CustomInput;
