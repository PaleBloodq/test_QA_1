import { Link } from "react-router-dom"
import Tag from "../../../components/common/Tag"
import { replaceUrl } from "../../../helpers/replaceUrl"

export default function SearchItem({ item }: { item: any }) {

    const baseLink = (() => {
        switch (item.product.type) {
            case "GAME":
                return `/game/${item.product.id}/${item.id}`
            case "SUBSCRIPTION":
                return `/subscription/${item.product.id}/${item.id}`
            case "DONATION":
                return `/donation/${item.product.id}`
            default:
                return "/";
        }
    })();


    return (
        <Link to={baseLink} className="w-[164px] h-fit flex flex-col justify-between items-start">
            <img className="w-[165px] h-[210px] object-cover rounded-xl" src={replaceUrl(item.product.type === 'GAME' ? item.search_image : item.product_page_image)} alt="Картинка" />
            <h1 className="mt-5 text-title">{item.product.title}</h1>
            <h2 className="text-subtitle">{item.title} {item.product.type === "SUBSCRIPTION" && item.duration + ' мес'}</h2>
            {
                item?.discount ? (
                    <div className="flex gap-2">
                        <h3 className="price-small">{item.final_price || item.original_price} ₽</h3>
                        <Tag type="discount">-{item?.discount}%</Tag>
                    </div>
                ) : (
                    <h3 className="price-small">{item?.original_price} ₽</h3>
                )
            }
        </Link>
    )
}
