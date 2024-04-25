import { SectionType } from '../../../types/SectionType'
import GamesSlider from '../../common/GamesSlider'
import useIsLoading from '../../../hooks/useIsLoading';

export default function Other({ data }: { data: SectionType[] }) {
    console.log(data)
    const isLoading = useIsLoading(data[0]?.objects);
    return (
        <div className='flex flex-col'>
            {
                data.map((item, index: number) => {
                    return (
                        <div key={index} className="mt-7 pt-6 pb-3 px-4 custom-border flex flex-col">
                            <div className="flex gap-3 items-center mb-4">
                                <h1 className="text-header">{item.name}</h1>
                            </div>
                            <GamesSlider type={item.objects[0].type} isLoading={isLoading} data={item.objects} />
                        </div>
                    )
                })
            }
        </div>
    )
}
