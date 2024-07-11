import { Link } from "react-router-dom";
import { replaceUrl } from "../../../helpers/replaceUrl";
import { Addon } from "../../../types/Addon";

export default function AddonCard({ addon }: { addon: Addon }) {
    return (
        <Link className="flex flex-col gap-2 w-[167px] custom-border p-2">
            <img className="w-full h-[200px] rounded-xl" src={replaceUrl(addon.product_page_image)} alt="addon" />
            <p className="text-subtitle-info">{addon.title}</p>
            <p className="text-subtitle">{addon.type}</p>
        </Link>
    )
}