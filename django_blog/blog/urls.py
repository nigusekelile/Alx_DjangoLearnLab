from taggit.models import Tag
from django.utils.text import slugify

def custom_tags_from_string(tag_string, tag_model=Tag):
    """
    Custom function to convert tag string to list of Tag objects
    """
    if not tag_string:
        return []
    
    tag_names = [name.strip() for name in tag_string.split(',') if name.strip()]
    
    # Get existing tags
    existing_tags = tag_model.objects.filter(name__in=tag_names)
    existing_tag_names = set(tag.name for tag in existing_tags)
    
    # Create new tags
    new_tags = []
    for name in tag_names:
        if name not in existing_tag_names:
            tag = tag_model(name=name)
            tag.save()
            new_tags.append(tag)
            existing_tag_names.add(name)
    
    # Return all tags
    return list(existing_tags) + new_tags

def custom_string_from_tags(tags):
    """
    Custom function to convert Tag objects to string
    """
    return ', '.join(tag.name for tag in tags)

def get_popular_tags(limit=10):
    """
    Get most popular tags based on usage count
    """
    from taggit.models import TaggedItem
    from django.db.models import Count
    
    popular_tags = Tag.objects.annotate(
        num_times=Count('taggit_taggeditem_items')
    ).order_by('-num_times')[:limit]
    
    return popular_tags

def get_tag_cloud(min_count=1, max_count=50):
    """
    Generate tag cloud data with sizes based on frequency
    """
    from taggit.models import TaggedItem
    from django.db.models import Count
    
    tags = Tag.objects.annotate(
        num_times=Count('taggit_taggeditem_items')
    ).filter(num_times__gte=min_count)
    
    if not tags:
        return []
    
    # Get min and max counts for scaling
    min_tag_count = min(tag.num_times for tag in tags)
    max_tag_count = max(tag.num_times for tag in tags)
    
    tag_cloud = []
    for tag in tags:
        # Calculate font size (1.0 to 3.0)
        if max_tag_count == min_tag_count:
            size = 2.0
        else:
            size = 1.0 + 2.0 * (tag.num_times - min_tag_count) / (max_tag_count - min_tag_count)
        
        tag_cloud.append({
            'tag': tag,
            'size': size,
            'count': tag.num_times,
        })
    
    return tag_cloud