import Tag from "../../../components/common/Tag"
import { getDiscount } from "../../../hooks/getDiscount"
import { SearchItemType } from "../../../types/searchItem"

export default function SearchItem({ item }: { item: SearchItemType }) {

    console.log(item)


    return (
        <div className="w-[165px] h-auto flex flex-col justify-between items-start">
            <img className="w-[165px] h-[210px] rounded-xl" src={item.photoUrls[0]} alt="Картинка" />
            <h1 className="mt-5 text-title">{item.title}</h1>
            <h2 className="text-subtitle">{item.pubTitle}</h2>
            {
                item?.discount?.percent ? (
                    <div className="flex gap-2">
                        <h3 className="price-small">{getDiscount((item?.prices[0]?.price), (item?.discount?.percent))} ₽</h3>
                        <Tag type="discount">-{item?.discount?.percent}%</Tag>
                    </div>
                ) : (
                    <h3 className="price-small">{item?.prices[0]?.price} ₽</h3>
                )
            }
        </div>
    )
}
