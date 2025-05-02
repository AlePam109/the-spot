export function getSession() {
    return {
        accountType: localStorage.getItem("accountType"),
        accountId: localStorage.getItem("accountId")
    };
}

export function isLoggedIn() {
    const { accountType, accountId } = getSession();
    return accountType && accountId;
}

export function clearSession() {
    localStorage.removeItem("accountType");
    localStorage.removeItem("accountId");
}
