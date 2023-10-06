export const checkPasswordPolicy = (password: string) => {
    if (password === "") {
        return true;
    }
    if (password.length < 8) {
        return false;
    }
    // Check if password contains at least one digit and one letter
    const hasDigit = /[0-9]/.test(password);
    const hasLetter = /[a-zA-Z]/.test(password);

    if (!hasDigit || !hasLetter) {
        return false;
    }
    return true;
};

export const checkPasswordAgain = (password1: string, password2: string) => {
    if (password1 === "" || password2 === "") {
        return true;
    }
    if (password1 !== password2) {
        return false;
    }
    return true;
};

export const checkEmail = (email: string) => {
    if (email === "") {
        return true;
    }
    // Regular expression for basic email validation
    const regex = /^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/;

    return regex.test(email);
};

export const checkName = (name: string) => {
    const hasHan = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(name);
    const notFullhan = /[ㄱ-ㅎ|ㅏ-ㅣ]/.test(name);

    if (name === "") {
        return true;
    }

    if (notFullhan) {
        return false;
    }

    if (hasHan && name.length >= 2) {
        return true;
    }
    return false;
};

export const checkEnName = (name: string) => {
    if (name === "") {
        return true;
    }
    const regex = /^[a-zA-Z\s]+$/;
    return regex.test(name);
};

export const checkPhone = (phone: string) => {
    if (phone === "") {
        return true;
    }
    const regex = /^\d{3}-\d{3,4}-\d{4}$/;
    return regex.test(phoneNumberAutoFormat(phone));
};

export const phoneNumberAutoFormat = (phoneNumber: string): string => {
    const number = phoneNumber?.trim().replace(/[^0-9]/g, "");

    if (number) {
        if (number.length < 4) return number;
        if (number.length < 7) return number.replace(/(\d{3})(\d{1})/, "$1-$2");
        if (number.length < 11) return number.replace(/(\d{3})(\d{3})(\d{1})/, "$1-$2-$3");
        return number.replace(/(\d{3})(\d{4})(\d{4})/, "$1-$2-$3");
    }
    return "";
};

export const checkCustomId = (customId: string) => {
    if (customId === "") {
        return true;
    }
    const regex = /^[a-zA-Z]{1}\d{9}$/;
    return regex.test(customId);
};

export const checkAddressValidation = (
    krName: string,
    enName: string,
    customId: string,
    phone: string,
    krAddress: string,
    enAddress: string
) => {
    if (krName === "" || enName === "" || customId === "" || phone === "" || krAddress === "" || enAddress === "") {
        return false;
    }
    return checkEnName(enName) && checkName(krName) && checkPhone(phone) && checkCustomId(customId);
};

export const checkCustomIdValidation = (customId: string, krName: string, phone: string) => {
    if (customId === "" || krName === "" || phone === "") {
        return false;
    }
    return checkName(krName) && checkPhone(phone) && checkCustomId(customId);
};

export const checkDefaultInputValidation = (email: string, name: string, password1: string, password2: string) => {
    if (email === "" || name === "" || password1 === "" || password2 === "") {
        return false;
    }
    return (
        checkEmail(email) &&
        checkName(name) &&
        checkPasswordPolicy(password1) &&
        checkPasswordAgain(password1, password2)
    );
};
