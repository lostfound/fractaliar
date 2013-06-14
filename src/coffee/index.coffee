th = @
set_events= =>
    $('.fractal_select').change ->
        n=$(@).find(':selected')[0].value
        fractal_node = $(@).parent().parent().find('.base_fractal')[0]
        $.get "fractal", { n }, (data)=>
            $(fractal_node).html(data)

    $('#Plus').click ->
        me = $(@).parent().parent()
        fr = me.parent().find('.base_fractal')[0]
        clone = $(fr).parent().clone()
        #$(clone, '#shape_select').find(':selected')[0].value = 2
        #$($(fr).parent(), '#shape_select').find(':selected')[0].value
        clone.appendTo(me.parent())
        v = $('.fractal_select', $(fr).parent() )[0].value
        $('.fractal_select', clone)[0].value = v
        me.clone().appendTo(me.parent())
        $(@).parent().parent().attr('class', 'plus')
        $(@).parent().parent().html('+')
        set_events()
    $('#RM').click ->
        flst = $('.fractal')
        if flst.length == 1
            return
        l = flst.length - 1
        $(flst[l]).remove()
        plst = $('.plus')
        $(plst[plst.length - 1 ]).remove()
    $('#EQ').click ->
        shape = $('#shape_select').find(':selected')[0].value
        fractals = null
        for fractal in $('.fractal_select')
            if fractals
                fractals += 'x'+ $(fractal).find(':selected')[0].value
            else
                fractals = $(fractal).find(':selected')[0].value
        params = { shape, fractals }
        if th.fractal_file
            params.layout = th.lno
            params.filename = th.fractal_file
        $.get "gen", params, (url)=>
            th.fractal_file = url
            $('#link').html('<a href="' + url + '">Fractal here</a>')
            $.get url, {}, (data) =>
                $('#result').html( (new XMLSerializer()).serializeToString(data) )
                if th.lno == undefined
                    th.layouts.push(new Layout(0))
                    th.lno = 0
                for l in layouts
                    l.set_transforms()
                    l.set_color(null)
                $('#result').children()[0].addEventListener('mousedown', onmousedown, false)
                $('#result').children()[0].addEventListener('mouseup', onmouseup, false)

mouse_is_down=false
down_xy=[0,0]
onmousedown=(e)=>
    #alert e.pageX+','+e.pageY
    down_xy = [e.pageX, e.pageY]
    mouse_is_down = true
onmouseup=(e)=>
    return if not mouse_is_down
    dlt = [ e.pageX - down_xy[0], e.pageY - down_xy[1]]
    layout().dragnmove(dlt)

class Layout
     constructor: (nu)->
        @nu = nu
        @xy    = [100,100]
        @step  = 3
        @scale_step = .3
        @scale = 3
        @stroke= 4
        @rotate= 0
        @color = 'black'
        @set_transforms= ->
            $('#ff'+@nu).attr('transform', 'translate(' + @xy[0] + ',' + @xy[1] + ') scale(' + @scale + ') rotate(' + @rotate + ')')
        @set_stroke=(stroke) ->
            @stroke = stroke
            $('#ff'+@nu).attr( 'stroke-width', @stroke )
        @inc_rotate=(dlt) ->
            @rotate -= dlt
            @set_transforms()
        @dragnmove= (dlt)->
            @xy[0]+=dlt[0]
            @xy[1]+=dlt[1]
            @set_transforms()
            
        @up= ->
            @xy[1]-=@step
            @set_transforms()
        @down= ->
            @xy[1]+=@step
            @set_transforms()
        @left= ->
            @xy[0]-=@step
            @set_transforms()
        @right= ->
            @xy[0]+=@step
            @set_transforms()
        @zoomin= ->
            @scale += .3
            @set_transforms()
        @zoomout= ->
            @scale -= .3
            @set_transforms()
        @set_color= (color) ->
            if color != null
                @color = color
            $('#ff'+@nu).attr('stroke', @color)
        return @


trfm = null
stroke=null
rotate=0
t=new Layout(0)
tt=new Layout(1)


@fractal_file = undefined
@lno = undefined
@layouts = []

@layout= =>
    return @layouts[@lno]
parse_transforms= =>
   t = $('#ff0').attr('transform')
   ts=t.split(',')
   x=parseInt(ts[0].split('(')[1])
   y=parseInt(ts[1].split(')')[0])
   scale=parseFloat(t.split('(')[2].split(')')[0])
   return [x,y,scale]

set_stroke=(w) =>
   $('#ff0').attr('stroke-width', w)
   stroke=w

$(document).ready =>
    $('#picker').farbtastic (cl)=>
        color = cl
        th.layout().set_color(cl)
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
        layout().up()
    $('#Down').click ->
        layout().down()
    $('#Left').click ->
        layout().left()
    $('#Right').click ->
        layout().right()
    $('#Zoomin').click ->
        layout().zoomin()
    $('#Zoomout').click ->
        layout().zoomout()
    $('#stroke').change ->
        layout().set_stroke $(@).find(':selected')[0].value
    $('#Rotate').click ->
        layout().inc_rotate(10)
    $('#deRotate').click ->
        layout().inc_rotate(-10)
    $('#Layout').change ->
        lv =  $(@).find(':selected')[0].value
        if lv == 'NEW'
            if th.lno == undefined
                return
            th.lno += 1
            th.layouts.push(new Layout(th.lno))
            $(@).find(':selected')[0].value = th.lno
            $($(@).find(':selected')[0]).html(th.lno)
            $(@).append($('<option value="NEW">New</option>'))
        else
            th.lno = parseInt(lv)

    set_events()
