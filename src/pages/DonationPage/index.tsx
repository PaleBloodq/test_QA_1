import { useParams } from "react-router";
import Container from "../../components/common/Container";
import { useGetAnyProductQuery } from "../../services/productsApi";
import DonationQuantity from "./DonationQuantity";
import { donationType } from "../../types/donationType";
import { useEffect, useState } from "react";
import Line from "../../components/common/Line";
import Button from "../../components/common/Button";

export default function DonationPage() {

    const { id } = useParams()

    const { data = {} as donationType, isLoading } = useGetAnyProductQuery(id);
    const [selectedQuantity, setSelectedQuantity] = useState(0)
    const [currentPrice, setCurrentPrice] = useState(data.unitPrice * selectedQuantity)
    useEffect(() => { setCurrentPrice(data.unitPrice * selectedQuantity) }, [selectedQuantity])

    console.log(data)

    return (
        <Container>
            <div className="flex flex-col items-center">
                {!isLoading &&
                    <div className="flex flex-col items-start w-full">
                        <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={data.photoUrls[0]} alt="donation image" />
                        <h1 className="text-header mb-2">{data.title}</h1>
                        <DonationQuantity selectedQuantity={selectedQuantity} setSelectedQuantity={setSelectedQuantity} quantitys={data.quantityVariations} />
                        <h2 className="text-subtitle mt-8 mb-2">Цена:</h2>
                        <h1 className="price-big">{currentPrice} ₽</h1>
                        <Line />
                        <div className='flex flex-col gap-2 w-full'>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Платформа:</p>
                                <p className='text-title text-[14px]'>{data.platforms.map((platform: string[]) => platform).join(', ')}</p>
                            </div>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Язык:</p>
                                <p className='text-title text-[14px]'>{data.languages.map((lang: string[]) => lang).join(', ')}</p>
                            </div>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Дата релиза:</p>
                                <p className='text-title text-[14px]'>{data.releaseDate}</p>
                            </div>
                        </div>
                        <Button onClick={() => console.log('click')}>Добавить в корзину</Button>
                    </div>
                }
            </div>
        </Container>
    )
}
