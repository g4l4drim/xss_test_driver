/**
 * Created by PyCharm.
 * User: eal
 * Date: 08/11/11
 * Time: 14:24
 * To change this template use File | Settings | File Templates.
 */
 //TODO: change display & data rendering using more sexy JS lib
function renderbw()
{
    //black & white rendering for table
    $('tr > td').each(function() {
        if ($(this).text() > 0) {
            $(this).addClass('pass')
        }
    })
}

function computewidth(){
    max=0;
    vheaders=$('th').filter(function(index){return index!=0})
    vheaders.each(function(){
        max=Math.max($(this).width(),max);
    })
    vheaders.width(max)
}

$(document).ready(function(){
    renderbw();
    computewidth();
})