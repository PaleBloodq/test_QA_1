import lightningIcon from "@icons/lightning.svg";

export default function NewGames() {
    return (
        <div className="mt-7 py-6 px-4 custom-border flex flex-col">
            <div className="flex gap-3 items-center">
                <img src={lightningIcon} alt="new" />
                <h1 className="text-subtitle">Новинки</h1>
            </div>
            <div></div>
        </div>
    )
}
