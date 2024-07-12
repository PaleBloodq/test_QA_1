import { useParams } from "react-router"
import { AddonType } from "../../types/AddonType";
import { useGetAddonQuery } from "../../services/productsApi";
import { replaceUrl } from "../../helpers/replaceUrl";
import AddToWishlist from "../../components/common/AddToWishlist";
import SelectPrice from "../../components/common/SelectPrice";
import Tag from "../../components/common/Tag";
import calcCashback from "../../helpers/calcCashback";
import Line from "../../components/common/Line";
import AddToCartButton from "../../components/common/AddToCartButton";

export default function Addon() {
    const id = useParams().id
    const { data = {} as AddonType, isLoading } = useGetAddonQuery(id);
    console.log(data)

    const includes = data.includes?.split("\r\n") || [];

    const cartItem = {
        id: data.id,
        type: data.type,
        img: data.product_page_image,
        title: data.title,
        publication: data.title,
        platform: '',
        price: data.final_price,
        final_price: data.final_price,
        discount: data.discount,
        cashback: data.cashback,
        product_type: data.product_type
    };

    return (
        <div>
            {!isLoading && (
                <div className="flex flex-col items-start w-full">
                    <img className="w-full h-[400px] mb-8 object-cover" src={replaceUrl(data.product_page_image)} alt="game image" />
                    <div className='w-full -mt-16 bg-white dark:bg-[#1a1e22] rounded-t-3xl px-3 py-1 mb-5'>
                        <div className='flex items-center gap-2'>
                            <h1 className="text-header">{data.title}</h1>
                            <AddToWishlist id={data.id} />
                        </div>
                        <div className="flex items-center flex-wrap w-full gap-2">
                            {!data.ps_plus_discount ? (
                                <h1 className="price-big">
                                    {data.final_price || 0} ₽
                                </h1>
                            ) : (
                                <SelectPrice price={data.ps_plus_final_price} discount={data.ps_plus_discount} />
                            )}
                            <div className="flex gap-2">
                                {data.ps_plus_discount === 0 && data.discount > 0 ? (
                                    <Tag type="discount">-{data.discount}%</Tag>
                                ) : null}
                                {data.cashback ? <Tag type="cashback">Кэшбэк: {calcCashback(data.final_price, data.cashback)} ₽</Tag> : null}
                            </div>
                            {data.discount ? (
                                <div className="w-full flex justify-between mb-5">
                                    <p className="text-subtitle">Скидка действует до:</p>
                                    <p className="text-subtitle-info">{data.discount_deadline}</p>
                                </div>
                            ) : null}
                            <Line />
                            {includes.length > 1 &&
                                <>
                                    <div className='flex flex-col'>
                                        <h1 className='text-title-xl mb-[20px]'>Состав издания:</h1>
                                        <ul className='list-disc ml-3'>
                                            {includes.map((item, index) => (
                                                <li key={index} className='custom-marker text-subtitle'>{item}</li>
                                            ))}
                                        </ul>
                                    </div>
                                    <Line />
                                </>
                            }
                            <div className='flex flex-col gap-2 w-full'>
                                <div className='w-full flex justify-between'>
                                    <p className='text-subtitle'>Платформа:</p>
                                    <p className='text-title text-[14px]'>{data.platforms.join(', ') || 'Нет данных'}</p>
                                </div>
                                <div className='w-full flex justify-between'>
                                    <p className='text-subtitle'>Язык:</p>
                                    <p className='text-title text-[14px]'>{data.languages.join(', ') || 'Нет данных'}</p>
                                </div>
                            </div>
                        </div>
                        <AddToCartButton cartItem={cartItem} />
                    </div>
                </div>
            )}

        </div>
    )
}
