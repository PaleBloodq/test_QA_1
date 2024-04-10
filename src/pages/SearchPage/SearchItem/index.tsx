export default function SearchItem({ item }) {
    console.log(item)
    return (
        <div className="w-full h-auto flex flex-col justify-between items-start">
            <img className="w-[165px] h-[210px] rounded-xl" src={item.photoUrls[0]} alt="Картинка" />
            <h1 className="mt-5 text-title">{item.title}</h1>
        </div>
    )
}
