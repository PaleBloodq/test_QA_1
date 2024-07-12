import { Link } from "react-router-dom";
import { replaceUrl } from "../../../helpers/replaceUrl";
import { AddonType } from "../../../types/AddonType";

export default function AddonCard({ addon }: { addon: AddonType }) {
    return (
        <Link to={`/addon/${addon.id}`} className="flex flex-col gap-2 w-[167px] custom-border p-2">
            <img className="w-full h-[200px] rounded-xl" src={replaceUrl(addon.product_page_image)} alt="addon" />
            <p className="text-subtitle-info">{addon.title}</p>
            <p className="text-subtitle">{addon.type}</p>
        </Link>
    )
}