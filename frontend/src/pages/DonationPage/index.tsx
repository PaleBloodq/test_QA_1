import { useParams } from "react-router";
import Container from "../../components/common/Container";
import { useGetAnyProductQuery } from "../../services/productsApi";
import DonationQuantity from "./DonationQuantity";
import { useEffect, useState } from "react";
import Line from "../../components/common/Line";
import { CartItemType } from "../../types/cartItem";
import AddToCartButton from "../../components/common/AddToCartButton";
import { ProductType } from "../../types/ProductType";
import { replaceUrl } from "../../helpers/replaceUrl";
import { Publication } from "../../types/PublicationType";
import Tag from "../../components/common/Tag";

export default function DonationPage() {

    const { id } = useParams()
    const { data = {} as ProductType, isLoading } = useGetAnyProductQuery(id);
    const [selectedQuantity, setSelectedQuantity] = useState(0)

    const [currentPublicaton, setCurrentSubscription] = useState(data?.publications?.find((item) => item?.quantity === selectedQuantity))

    useEffect(() => {
        if (data?.publications) {
            const foundPublication = data.publications.find((item) => item?.quantity === selectedQuantity);
            setCurrentSubscription(foundPublication ?? currentPublicaton);
        }
    }, [data?.publications, selectedQuantity, currentPublicaton]);

    const currentPrice = (currentPublicaton && currentPublicaton.final_price) || 0;

    const cartItem: CartItemType = {
        id: currentPublicaton?.id,
        type: "DONATION",
        img: currentPublicaton?.preview,
        title: data?.title,
        publication: `${selectedQuantity} шт`,
        platform: currentPublicaton?.platforms?.map((platform) => platform).join(', '),
        price: currentPrice,
        final_price: currentPrice,
        discount: currentPublicaton?.discount,
        cashback: currentPublicaton?.cashback
    }



    return (
        <Container>
            <div className="flex flex-col items-center">
                {!isLoading &&
                    <div className="flex flex-col items-start w-full">
                        <img className="w-full h-[400px] rounded-xl mb-8 object-cover" src={replaceUrl(data?.publications[0]?.photo)} alt="donation image" />
                        <h1 className="text-header mb-2">{data?.title}</h1>
                        <DonationQuantity selectedQuantity={selectedQuantity} setSelectedQuantity={setSelectedQuantity} quantitys={data?.publications?.map((pub: Publication) => pub?.quantity)} />
                        <h2 className="text-subtitle mt-8 mb-2">Цена:</h2>
                        <div className="flex gap-2 items-center">
                            <h1 className="price-big">{currentPrice} ₽</h1>
                            {currentPublicaton?.discount ? <Tag type="discount">-{currentPublicaton?.discount}%</Tag> : null}

                        </div>
                        <Line />
                        <div className='flex flex-col gap-2 w-full'>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Платформа:</p>
                                <p className='text-title text-[14px]'>{currentPublicaton?.platforms.map((platform) => platform)?.join(', ')}</p>
                            </div>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Язык:</p>
                                <p className='text-title text-[14px]'>{currentPublicaton?.languages.map((lang) => lang)?.join(', ')}</p>
                            </div>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Дата релиза:</p>
                                <p className='text-title text-[14px]'>{data?.release_date || 'Нет данных'}</p>
                            </div>
                        </div>
                        <AddToCartButton cartItem={cartItem} />
                    </div>
                }
            </div>
        </Container>
    )
}
