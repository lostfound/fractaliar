set_events= =>
    $('.fractal_select').change ->
        n=$(@).find(':selected')[0].value
        fractal_node = $(@).parent().parent().find('.base_fractal')[0]
        $.get "fractal", { n }, (data)=>
            $(fractal_node).html(data)

    $('#Plus').click ->
        me = $(@).parent().parent()
        fr = me.parent().find('.base_fractal')[0]
        $(fr).parent().clone().appendTo(me.parent())
        me.clone().appendTo(me.parent())
        $(@).parent().parent().html('+')
        set_events()
    $('#EQ').click ->
        shape = $('#shape_select').find(':selected')[0].value
        fractals = null
        for fractal in $('.fractal_select')
            if fractals
                fractals += 'x'+ $(fractal).find(':selected')[0].value
            else
                fractals = $(fractal).find(':selected')[0].value
        $.get "gen", { shape, fractals }, (url)=>
            $('#link').html('<a href="' + url + '">Fractal here</a>')
            $.get url, {}, (data) =>
                $('#result').html( (new XMLSerializer()).serializeToString(data) )
                if trfm
                    set_transforms(trfm)
                if stroke
                    set_stroke(stroke)
trfm = null
stroke=null
parse_transforms= =>
   t = $('#ff').attr('transform')
   ts=t.split(',')
   x=parseInt(ts[0].split('(')[1])
   y=parseInt(ts[1].split(')')[0])
   scale=parseFloat(t.split('(')[2].split(')')[0])
   return [x,y,scale]

set_stroke=(w) =>
   $('#ff').attr('stroke-width', w)
   stroke=w

set_transforms=(ts) =>
    trfm = ts
    $('#ff').attr('transform', 'translate('+ts[0]+','+ts[1]+') scale('+ts[2]+')')

$(document).ready =>
    n=$('#shape_select')[0].value
    $.get "shape", { n }, (data)=>
        $('#base_shape').html(data)

    n=$('.fractal_select').find(':selected')[0].value
    fractal_node = $('.fractal_select').parent().parent().find('.base_fractal')[0]
    $.get "fractal", { n }, (data)=>
        $(fractal_node).html(data)

    $('#shape_select').change ->
        n=$(@).find(':selected')[0].value
        $.get "shape", { n }, (data)=>
            $('#base_shape').html(data)

    $('#Up').click ->
        ts = parse_transforms()
        ts[1]-=3
        set_transforms(ts)

    $('#Down').click ->
        ts = parse_transforms()
        ts[1]+=3
        set_transforms(ts)
    $('#Left').click ->
        ts = parse_transforms()
        ts[0]-=3
        set_transforms(ts)
    $('#Right').click ->
        ts = parse_transforms()
        ts[0]+=3
        set_transforms(ts)
    $('#Zoomin').click ->
        ts = parse_transforms()
        ts[2]+=.3
        set_transforms(ts)
    $('#Zoomout').click ->
        ts = parse_transforms()
        ts[2]-=.3
        set_transforms(ts)
    $('#stroke').change ->
        w=$(@).find(':selected')[0].value
        set_stroke(w)

        
        
        
    set_events()
