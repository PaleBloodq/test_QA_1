import { useEffect } from "react";

type Props = {
    quantitys: number[];
    selectedQuantity: number;
    setSelectedQuantity: (quantity: number) => void;
}


export default function DonationQuantity({ quantitys, selectedQuantity, setSelectedQuantity }: Props) {

    useEffect(() => {
        setSelectedQuantity(quantitys[0])
    }, [])

    return (
        <div className="w-full mt-3 flex-col gap-6">
            <h1 className="text-title-xl mb-5">Количество</h1>
            <div className="w-full overflow-x-scroll flex gap-2">
                {quantitys.map((quantity, index) => {
                    return (
                        <button
                            onClick={() => setSelectedQuantity(quantity)}
                            key={index}
                            className={`w-20 h-12 flex flex-col flex-shrink-0 justify-center items-center ${selectedQuantity == quantity ? 'custom-border__red' : 'custom-border'}`}
                        >
                            <h2 className="price-small">
                                {quantity}
                            </h2>
                        </button>
                    )
                })}
            </div>
        </div>
    )
}
