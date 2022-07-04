<?php
require __DIR__ . "/vendor/autoload.php";
include_once('vendor/simplehtmldom/simplehtmldom/simple_html_dom.php');

$queryParam = $_POST['article'];
$url = "https://www.autozap.ru/goods?code=$queryParam&count=300&page=1&search=Найти";

$html = file_get_html($url);

if ($html->find('h3', 0) != "") {
    $itemsUrl = "https://www.autozap.ru" . $html->find("tr[onclick=document.getElementById('goodLnk1').click();] a", 0)->href;
    $html = file_get_html($itemsUrl);
    $data = parseProducts($html);
} elseif ($html->find("h4")[0] != "") {
    $data = parseProducts($html);
}

$json = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
file_put_contents("$queryParam.json", $json);
header('Location: index.php');
exit();

function parseProducts($html)
{
    $trs = $html->find("table tr[style= background:none;],tr[style= ]");
    $array = array();
    $currentName = '';
    foreach ($trs as $key => $value) {
        $itemNum = $key + 1;
        $curName = $value->find("a", 0)->plaintext;
        if ($curName != "")
            $currentName = $curName;
        $article = $value->find("input[id=ecomCode$itemNum]", 0)->value;
        $brand = $value->find("input[id=ecomManuf$itemNum]", 0)->value;
        $id = $value->find("input[id=g$itemNum]", 0)->value;
        $count = $value->find("span[href=#]", 0)->plaintext;
        $time = $value->find("td[class=hidden-sm hidden-xs article]", 0)->plaintext;
        $price = $value->find("span[id=sp$itemNum]", 0)->plaintext;
        if ($time == 'Ожидается')
            $time = 'Ожидается';
        else
            $time = preg_replace('/[^0-9]/', '', $time);
        $array[] = array(
            "name" => $currentName,
            "price" => $price,
            "article" => $article,
            "brand" => $brand,
            "count" => $count,
            "time" => intval($time),
            "id" => $id
        );
    }
    return $array;
}
?>